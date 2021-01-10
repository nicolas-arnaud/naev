/*
 * See Licensing and Copyright notice in naev.h
 */

/**
 * @file nlua_rnd.c
 *
 * @brief Lua bindings for the Naev random number generator.
 */

/** @cond */
#include <lauxlib.h>

#include "naev.h"
/** @endcond */

#include "nlua_rnd.h"

#include "log.h"
#include "map.h"
#include "ndata.h"
#include "nluadef.h"
#include "rng.h"


/* Random methods. */
static int rnd_int( lua_State *L );
static int rnd_sigma( lua_State *L );
static int rnd_twosigma( lua_State *L );
static int rnd_threesigma( lua_State *L );
static int rnd_permutation( lua_State *L );
static const luaL_Reg rnd_methods[] = {
   { "int", rnd_int }, /* obsolete, rnd.rnd is preferred. */
   { "rnd", rnd_int },
   { "sigma", rnd_sigma },
   { "twosigma", rnd_twosigma },
   { "threesigma", rnd_threesigma },
   { "permutation", rnd_permutation },
   {0,0}
}; /**< Random Lua methods. */


/**
 * @brief Loads the Random Number Lua library.
 *
 *    @param env Lua environment.
 *    @return 0 on success.
 */
int nlua_loadRnd( nlua_env env )
{
   nlua_register(env, "rnd", rnd_methods, 0);
   return 0;
}


/**
 * @brief Bindings for interacting with the random number generator.
 *
 * This module not only allows basic random number generation, but it also
 *  handles more complicated statistical stuff.
 *
 * Example usage would be:
 * @code
 * if rnd.rnd() < 0.5 then
 *    -- 50% chance of this happening
 * else
 *    -- And 50% chance of this happening
 * end
 * @endcode
 *
 * @luamod rnd
 */
/**
 * @brief Gets a random number.  With no parameters it returns a random float between
 *  0 and 1.
 *
 * With one parameter it returns a whole number between 0 and that number
 *  (both included).  With two parameters it returns a whole number between
 *  both parameters (both included).
 *
 * @usage n = rnd() -- Number in range [0:1].
 * @usage n = rnd(5) -- Number in range [0:5].
 * @usage n = rnd(3,5) -- Number in range [3,5].
 *
 *    @luatparam number x First parameter, read description for details.
 *    @luatparam number y Second parameter, read description for details.
 *    @luatreturn number A randomly generated number, read description for details.
 * @luafunc rnd
 */
static int rnd_int( lua_State *L )
{
   int o;
   int l,h;

   o = lua_gettop(L);

   if (o==0)
      lua_pushnumber(L, RNGF() ); /* random double 0 <= x <= 1 */
   else if (o==1) { /* random int 0 <= x <= parameter */
      l = luaL_checkint(L,1);
      lua_pushnumber(L, RNG(0, l));
   }
   else if (o>=2) { /* random int parameter 1 <= x <= parameter 2 */
      l = luaL_checkint(L,1);
      h = luaL_checkint(L,2);
      lua_pushnumber(L, RNG(l,h));
   }
   else NLUA_INVALID_PARAMETER(L);

   return 1; /* unless it's returned 0 already it'll always return a parameter */
}
/**
 * @brief Creates a number in the one-sigma range [-1:1].
 *
 * A one sigma range means that it creates a number following the normal distribution
 *  but limited to the 63% quadrant.  This means that the number is biased towards 0,
 *  but can become either 1 or -1.  It's a fancier way of generating random numbers.
 *
 * @usage n = 5.5 + rnd.sigma()/2. -- Creates a number from 5 to 6 slightly biased to 5.5.
 *    @luatreturn number A number from [-1:1] biased slightly towards 0.
 * @luafunc sigma
 */
static int rnd_sigma( lua_State *L )
{
   lua_pushnumber(L, RNG_1SIGMA());
   return 1;
}
/**
 * @brief Creates a number in the two-sigma range [-2:2].
 *
 * This function behaves much like the rnd.sigma function but uses the two-sigma range,
 *  meaning that numbers are in the 95% quadrant and thus are much more random.  They are
 *  biased towards 0 and approximately 63% will be within [-1:1].  The rest will be in
 *  either the [-2:-1] range or the [1:2] range.
 *
 * @usage n = 5.5 + rnd.twosigma()/4. -- Creates a number from 5 to 6 heavily biased to 5.5.
 *
 *    @luatreturn number A number from [-2:2] biased heavily towards 0.
 * @luafunc twosigma
 */
static int rnd_twosigma( lua_State *L )
{
   lua_pushnumber(L, RNG_2SIGMA());
   return 1;
}
/**
 * @brief Creates a number in the three-sigma range [-3:3].
 *
 * This function behaves much like its brothers rnd.sigma and rnd.twosigma.  The main
 *  difference is that it uses the three-sigma range which is the 99% quadrant.  It
 *  will rarely generate numbers outside the [-2:2] range (about 5% of the time) and
 *  create numbers outside of the [-1:1] range about 37% of the time.  This can be used
 *  when you want extremes to appear rarely.
 *
 * @usage n = 5.5 + rnd.threesigma()/6. -- Creates a number from 5 to 6 totally biased to 5.5.
 *
 *    @luatreturn number A number from [-3:3] biased totally towards 0.
 * @luafunc threesigma
 */
static int rnd_threesigma( lua_State *L )
{
   lua_pushnumber(L, RNG_3SIGMA());
   return 1;
}


/**
 * @brief Creates a random permutation
 *
 * This creates a list from 1 to input and then randomly permutates it,
 * however, if an ordered table is passed as a parameter, that is randomly
 * permuted instead.
 *
 * @usage t = rnd.permutation( 5 )
 * @usage t = rnd.permutation( {"cat", "dog", "cheese"} )
 *
 *    @luatparam number|table input Maximum value to permutate to.
 *    @luatreturn table A randomly permutated table.
 * @luafunc permutation
 */
static int rnd_permutation( lua_State *L )
{
   int *values;
   int i, j, temp, max;
   int new_table;

   NLUA_MIN_ARGS(1);
   if (lua_isnumber(L,1)) {
      max = lua_tointeger(L,1);
      new_table = 1;
   }
   else if (lua_istable(L,1)) {
      max = (int) lua_objlen(L,1);
      new_table = 0;
   }
   else
      NLUA_INVALID_PARAMETER(L);

   /* Create the list. */
   values = malloc( sizeof(int)*max );
   for (i=0; i<max; i++)
      values[i]=i;

   /* Fisher-Yates shuffling algorithm */
   for (i = max-1; i >= 0; --i){
      /* Generate a random number in the range [0, max-1] */
      j = randint() % (i+1);

      /* Swap the last element with an element at a random index. */
      temp      = values[i];
      values[i] = values[j];
      values[j] = temp;
   }

   /* Now either return a new table or permute the given table. */
   lua_newtable(L);
   for (i=0; i<max; i++) {
      lua_pushnumber( L, i+1 );
      lua_pushnumber( L, values[i]+1 );
      if (!new_table)
         lua_gettable(   L, 1 );
      lua_settable(   L, -3 );
   }

   free( values );

   return 1;
}

