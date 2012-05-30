# Calculating PI up to system's float precision
# Using several algorithms

# Archimedes (~250 BC)
# - lower bound: inscribed N-polygon semiperimeter
# - upper bound: circumscribed N-polygon semiperimeter

# Liu Hui (~265 AD)
#  lower bound: inscribed N-polygon area
#  upper bound: inscribed N-polygon area + N * (r-h)*l rectangle "tabs"


import sys

from math import sqrt as sqrt # use only root, and nothing else

# As reference, from Wikipedia.
# math.pi gives same value up to 15 digits if standard float arithmetic is used
refpi = 3.141592653589793238462643383279502884197169399375105820974944592307816

# Same as math.sqrt(3) up to float precision
sqrt3 = 1.73205080756887729352744634150587236694280525381038062805580

p = "15" # 64-bit IEEE-754 decimal precision, as string for easy concatenation

lbound = 0
ubound = sys.maxint # could also be 4

radius = 1

def _print_pi(i, n, l, u, pi):
    print (("{i:2d}: n={n:11,d} :"
            " {l:."+p+"f} < pi < {u:."+p+"f}, pi={pi:."+p+"f}"
            " (e={e:."+p+"%})").format(i=i, n=n, l=l, u=u, pi=pi, e=1-(pi/refpi)))

def ArchimedesPi():

    def _pi(n, iBC, iAB, iAC, cOC, cAC, cOA, oldpi=lbound, i=0):

        iedge = iBC
        cedge = 2 * cAC

        iperim = n * iedge / 2
        cperim = n * cedge / 2

        pi = (iperim + cperim) / 2

        _print_pi(i,n, iperim, cperim, pi)

        # was result the same within p significant digits?
        if ("{0:."+p+"f}").format(pi) == ("{0:."+p+"f}").format(oldpi):
            return pi

        # next inscribed edge (BD, the new BC)
        # (AB + AC) / BC = AD / DB
        # AD^2 + DB^2 = AB^2, ADB is a right triangle
        # solving for BD == edge == new iBC
        iBC = iBC * iAB / sqrt(iBC**2 + (iAB+iAC)**2)

        # other values
        iAB = iAB # never changes
        iAC = sqrt(iAB**2 - iBC**2) # from right triangle formulae

        # next circumscribed edge (2*AD, the new AC)
        # (CO + OA) / CA = OA / AD
        # OA^2 + AD^2 = DO^2
        # solving for AD == edge/2
        cAC = cOA * cAC / (cOC + cOA)

        # other values
        cOA = cOA # never changes
        cOC = sqrt(cAC**2 + cOA**2)

        return _pi(n*2, iBC, iAB, iAC, cOC, cAC, cOA, pi, i+1)

    # start with an hexagon
    n = 6

    # inscribed
    # A, B - opposite vertexes (polygon "diagonal": AB == diameter)
    # C - "next vertex" from B (BC == polygon edge)
    # OAC is a right triangle, hip=2*AC, OC=R
    iBC = radius # edge
    iAB = iBC * 2
    iAC = iBC * sqrt(3) # Archimedes used 1351/780 > sqrt(3) > 265/153

    # circumscribed
    # O - center
    # A - tangent point (polygon edge midpoint)
    # C - A's edge vertex (AC is half a side)
    # OAC is proportional to inscribed's ACB, so similar rules apply
    cOA = radius
    cAC = cOA / sqrt(3)
    cOC = 2 * cAC # edge

    return _pi(n, iBC, iAB, iAC, cOC, cAC, cOA)


print(("pi = {0:."+p+"f} (calculated)").format(ArchimedesPi()))
print(("pi = {0:."+p+"f} (reference)").format(refpi))
