# Calculating PI up to system's float precision
# Using several algorithms

# Archimedes (~250 BC)
# - lower bound: inscribed N-polygon semiperimeter
# - upper bound: circumscribed N-polygon semiperimeter

# Liu Hui (~265 AD)
#  lower bound: inscribed N-polygon area
#  upper bound: inscribed N-polygon area + N * (r-h)*l rectangle "tabs"

import sys

#from math import sqrt # use only root, and nothing else
from decimal import Decimal as D, getcontext

#precision = 15 # 64-bit IEEE-754 float decimal precision practical limit
precision  = 64 # Decimal module allows arbitrary precision (default = 28)
getcontext().prec = precision + 2 # some room for rounding cumulative errors

# Precision as string to allow easy concatenations on format()'s width
p = str(precision)

# As reference, from Wikipedia.
# math.pi is correct only up to 15 digits, due to standard float arithmetic
pistr = '3.1415926535897932384626433832795028841971693993751058209749445923'
#piref = math.pi
piref = D(pistr)

# Archimedes used 1351/780 > sqrt(3) > 265/153
# math.sqrt(3) not used for same reasons as pi
#sqrt3 = sqrt(3)
#sqrt3 = D('1.73205080756887729352744634150587236694280525381038062805580')
sqrt3 = D(3).sqrt()


lbound = 0
ubound = sys.maxint # could also be 4

radius = D(1)

def _print_pi(i, n, l, u, pi):
    print (("{i:2d}: n={n:"+str(int(precision/2.7)+1)+",d} :" # empyrical
            " {l:."+p+"f} ({el:+.2e}%)"
            " < pi <"
            " {u:."+p+"f} ({eu:+.2e}%)"
            " pi={pi:."+p+"f}"
            " ({ep:+.2e}%)").format(i=i, n=n, l=l, u=u, pi=pi,
                                 el=100*(( l/piref)-1),
                                 eu=100*(( u/piref)-1),
                                 ep=100*((pi/piref)-1),
                                ))

def ArchimedesPi():

    def _pi(n, iBC, iAC, cOC, cAC, oldpi=lbound, i=0):

        iedge = iBC
        cedge = 2 * cAC

        iperim = n * iedge / 2
        cperim = n * cedge / 2

        pi = (iperim * 2 + cperim) / 3 # inscribed is twice as better

        _print_pi(i,n, iperim, cperim, pi)

        # was result the same within p significant digits?
        if pi == oldpi:
            return pi

        # next inscribed edge (BD, the new BC)
        # (AB + AC) / BC = AD / DB
        # AD^2 + DB^2 = AB^2, ADB is a right triangle
        # solving for BD == edge == new iBC
        iBC = iBC * 2*radius / (iBC**2 + (2*radius + iAC)**2).sqrt()
        iAC = ((2*radius)**2 - iBC**2).sqrt() # from right triangle formulae

        # next circumscribed edge (2*AD, the new AC)
        # (CO + OA) / CA = OA / AD
        # OA^2 + AD^2 = DO^2
        # solving for AD == edge/2 == new cAC
        cAC = radius * cAC / (cOC + radius)
        cOC = (cAC**2 + radius**2).sqrt()

        return _pi(n*2, iBC, iAC, cOC, cAC, pi, i+1)

    # start with an hexagon
    n = 6

    # inscribed
    # A, B - opposite vertexes (polygon "diagonal": AB == diameter)
    # C - "next vertex" from B (BC == polygon edge)
    # OAC is a right triangle, hip=2*AC, OC=R
    iAC = radius * sqrt3
    iBC = radius # edge

    # circumscribed
    # O - center
    # A - tangent point (polygon edge midpoint)
    # C - A's edge vertex (AC is half a side)
    # OAC is proportional to inscribed's ACB, so similar rules apply
    cAC = radius / sqrt3
    cOC = 2 * cAC # edge

    return _pi(n, iBC, iAC, cOC, cAC)


print(("pi = {0:."+p+"f} (calculated)").format(ArchimedesPi()))
print(("pi = {0:."+p+"f} (reference)").format(piref))
print(("pi = {0} (string)").format(pistr[:precision+2]))
