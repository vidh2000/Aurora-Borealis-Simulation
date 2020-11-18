from vpython import *
from vector import *
from scattering import scatter

electron = sphere(pos = vector(0, 0, 100), make_trail = True)

B = lambda h: Vector(0, 0, 0) - Khat

P = Vector(0, 0, 100)

L = 1000

t = 0

while True:
    rate(3)
    P, t = scatter(P, B, L, t)
    electron.pos = vector(P.x, P.y, P.z)