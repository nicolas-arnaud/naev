#!/usr/bin/python3

N_ = lambda text: text
TEMPLATEPATH = "./templates/"

def lerpr( a, b ):
    return lambda x: int(round(a + x * (b-a)))

def lerp( a, b ):
    return lambda x: a + x * (b-a)

class BioOutfit:
    def __init__( self, template, params ):
        self.template = template
        self.params = params
        with open(TEMPLATEPATH+template,"r") as f:
            self.txt = f.read()

    def run(self, names):
        for k,n in enumerate(names):
            x = 1 if len(names)==1 else k/(len(names)-1)
            p = {k: v(x) if callable(v) else v for k, v in self.params.items()}
            p["name"]  = n
            with open( f"{n.lower().replace(' ','_')}.xml", "w" ) as f:
                txt = self.txt.format(**p)
                txt = txt.replace( "<general>", "<!-- THIS OUTFIT IS AUTOGENERATED. DO NOT EDIT DIRECTLY! -->\n <general>" )
                f.write( txt )

"""
pincer
stinger
barb
fang
talon
claw
"""

"""
Perlevis (ul)
Laevis (l)
Mediocris (m)
Largus (hm)
Ponderosus (h)
Immanis (uh)

Cerebrum -> nominative neutral
    perleve
    laevum
    mediocre
    largum
    ponderosum
    immane

Cortex -> nominative masculine
    perlevis
    laevis
    mediocris
    largus
    ponderosus
    immanis
"""

desc = {}
desc["brain"] = N_("The brain is a Soromid bioship's equivalent to core systems in synthetic ships. Possibly the most important organ, the brain provides processing power and allocates energy to the rest of the organism. All brains start off undeveloped, but over time, just like the ships themselves, they grow and improve.")
desc["engine"] = N_("The gene drive is a Soromid bioship's equivalent to engines in synthetic ships. It is charged with moving the organism through space and is even capable of hyperspace travel. All gene drives start off undeveloped, but over time, just like the ships themselves, they grow and improve.")
desc["hull"] = N_("The shell is a Soromid bioship's natural protection, equivalent to hulls of synthetic ships. The shell is responsible both for protecting the organism's internal organs and for creating camouflage to reduce the risk of being detected by hostiles. All shells start off undeveloped, but over time, just like the ships themselves, they grow and improve.")

typename = {}
typename["brain"] = N_("Bioship Brain")
typename["engine"] = N_("Bioship Gene Drive")
typename["hull"] = N_("Bioship Shell")

BioOutfit( "pincer.xml.template", {
    "price" :   lerpr(   0, 20e3 ),
    "damage":   lerp(    8,  17 ),
    "energy":   4,
    "range" :   lerp(  750, 900 ),
    "falloff":  lerp(  450, 750 ),
    "speed" :   lerp(  550, 700 ),
    "heatup":   lerp(   25,  40 ),
    "typename": N_("Bioship Weapon Organ"),
    "desc":     N_("The Pincer Organ is able to convert energy into hot plasma that is able to eat easily eat through shield and armour of opposing ships. While not an especially powerful offensive organ, it is prized for its reliability."),
} ).run( [N_("Pincer Organ I"), N_("Pincer Organ II")] )

BioOutfit( "perleve_cerebrum.xml.template", {
    "price":        lerpr(   0, 120e3 ),
    "mass":         14,
    "desc":         desc["brain"],
    "typename":     typename["brain"],
    "cpu":          lerpr(   3,   8 ),
    "shield" :      lerp(  160, 250 ),
    "shield_regen": lerp(    5,   9 ),
    "energy":       lerp(  130, 250 ),
    "energy_regen": lerp(   12,  19 ),
} ).run( [N_("Perleve Cerebrum I"), N_("Perleve Cerebrum II")] )

BioOutfit( "perlevis_gene_drive.xml.template", {
    "price":        lerpr(   0, 140e3 ),
    "mass":         8,
    "desc":         desc["engine"],
    "typename":     typename["engine"],
    "thrust":       lerp(  145, 196 ),
    "turn":         lerp(  120, 160 ),
    "speed":        lerp(  255, 345 ),
    "fuel":         400,
    "energy_malus": lerp(    5,   5 ),
    "engine_limit": lerp(  150, 150 ),
} ).run( [N_("Perlevis Gene Drive I"), N_("Perlevis Gene Drive II")] )

BioOutfit( "perlevis_cortex.xml.template", {
    "price":        lerpr(   0, 130e3 ),
    "mass":         30,
    "desc":         desc["hull"],
    "typename":     typename["hull"],
    "cargo":        lerpr(   4, 4 ),
    "absorb":       lerpr(   0, 3 ),
    "armour":       lerp(   45, 65 )
} ).run( [N_("Perlevis Cortex I"), N_("Perlevis Cortex II")] )

BioOutfit( "immane_cerebrum.xml.template", {
    "price":        lerpr(   0, 4e6 ),
    "mass":         1400,
    "desc":         desc["brain"],
    "typename":     typename["brain"],
    "cpu":          lerpr( 500, 1800 ),
    "shield" :      lerp(  700, 1200 ),
    "shield_regen": lerp(   12,  22 ),
    "energy":       lerp( 3000, 5250 ),
    "energy_regen": lerp(  135, 170 ),
} ).run( [N_("Immane Cerebrum I"), N_("Immane Cerebrum II"), N_("Immane Cerebrum III")] )

BioOutfit( "immanis_gene_drive.xml.template", {
    "price":        lerpr(   0, 3.6e6 ),
    "mass":         80,
    "desc":         desc["engine"],
    "typename":     typename["engine"],
    "thrust":       lerp(   31,  45 ),
    "turn":         lerp(   34,  55 ),
    "speed":        lerp(   61,  75 ),
    "fuel":         1600,
    "energy_malus": lerp(   50,  50 ),
    "engine_limit": lerp( 6500, 6500 ),
} ).run( [N_("Immanis Gene Drive I"), N_("Immanis Gene Drive II"), N_("Immanis Gene Drive III")] )

BioOutfit( "immanis_cortex.xml.template", {
    "price":        lerpr(   0, 2.9e6 ),
    "mass":         1950,
    "desc":         desc["hull"],
    "typename":     typename["hull"],
    "cargo":        lerpr(  90, 90 ),
    "absorb":       lerpr(  59, 80 ),
    "armour":       lerp( 1700, 2400 )
} ).run( [N_("Immanis Cortex I"), N_("Immanis Cortex II"), N_("Immanis Cortex III")] )

BioOutfit( "claw.xml.template", {
    "price" :   lerpr(   0, 125e3 ),
    "desc":     N_("The Claw Organ has the distinction of being the only fully rotating organic weapon while boasting a fully developed power output that is hard to beat with conventional weaponry found throughout the galaxy. The large globs of hot plasma it launches can corrode through even the strongest of armours."),
    "damage":   lerp(   40,  80 ),
    "energy":   174,
    "range" :   lerp( 1700, 2400 ),
    "falloff":  lerp( 1100, 1800 ),
    "speed" :   lerp(  425, 600 ),
    "heatup":   lerp(   25,  60 ),
    "typename": N_("Bioship Weapon Organ"),
} ).run( [N_("Claw Organ I"), N_("Claw Organ II"), N_("Claw Organ III"), N_("Claw Organ IV")] )
