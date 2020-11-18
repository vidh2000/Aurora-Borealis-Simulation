from random import uniform
import math
from vector import *

def scatter(P, B, L, t):
    h = P.z

    alpha_d = lambda h: 3 * math.pi / 180 # math.asin(B(h).getMagnitude() / B(100).getMagnitude())

    dt = 1 / 300
    delta_alpha = 0.015

    nu = uniform(0, 1)

    t += dt * nu

    P_new = P + B(h).normalize()

    Vt = P_new - P

    alpha = uniform(0, alpha_d(h) - t * delta_alpha)
    beta = uniform(0, 2 * math.pi)

    perp = Vector(Vt.z, 0, -Vt.x).normalize()
    Vp = Vt.rotateAboutAxis(perp, alpha)
    Vp = Vp.rotateAboutAxis(Vt.normalize(), beta)
    Vp = Vp.setMagnitude(L * dt * nu / math.cos(alpha))

    P = P + Vp
    

    return P, t

