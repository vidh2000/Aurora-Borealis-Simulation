from vpython import *
from random import uniform, choices
import math
from vector import *
import scipy as sp
import matplotlib.pyplot as plt

# Define a dictionary of colours
cols = {"red": vector(1, 0.31, 0.000001), 
        "blue": vector(0.278, 0.000001, 1),
        "green": vector(0.6814285714285721, 1, 0.000001)}

# Get air data
height, _, _, PN, PO, total = sp.loadtxt("data/density_and_concentration_data.csv", skiprows = 1, delimiter = ",", unpack = True)

normalised_total = (total / total[0])**0.125

# NOTE: 8th root taken as ration of densities exceed 10e9

def gamma(x):
    try:
        return math.gamma(x)
    except:
        return 1e5


def poisson(lm, sf, c, s):
    return lambda x: sf * lm**(c * x + s) * math.exp(-lm) / (gamma(c * x + s + 1))

def green(x):
    try:
        return poisson(1.7, 230, 1/23, 0)(x - 100 - 12)
    except:
        print(x)

def blue(x):
    try:
        return poisson(1.7, 115, 1/23, 0)(x -100 - 12)
    except:
        print(x)

def red(x):
    try: 
        return poisson(7, 90, 1/23, 0)(x -100 - 12)
    except:
        print(x)

def total(x):
    return (green(x) + blue(x) + red(x)) / 110

# # DEBUGGING ONLY
# x = np.linspace(100, 300, 100)
# y1 = list(map(green, x))
# y2 = list(map(red, x))
# y3 = list(map(blue, x))
# y4 = list(map(total, x))
# plt.plot(x, y1, c = "green")
# plt.plot(x, y2, c = "red")
# plt.plot(x, y3, c = "blue")
# plt.plot(x, y4, c = "orange")
# plt.xlabel("Altitude / km")
# plt.ylabel("Intensity / Arbitrary units")
# plt.show()

def round_to_nearest(x, n):
    r = int(x) % n
    if r <= n / 2:
        return int(x - r)
    else:
        return int(x + n - r)


def get_color(h):
    # h = round_to_nearest(h, 10)
    # for i in range(len(height)):
    #     if height[i] == h:
    #         index = i
    #         break
    choice = ["red", "green", "blue"]
    # weights = [PO[index], PN[index] * 2 / 3, PN[index] / 3]
    weights = [max(red(h), 0.1), max(green(h), 0.1), max(blue(h), 0.1)]
    return choices(choice, weights)[0]

#Characteristics
r = 0.3
o = 0.08

def opacity(h):
    if cols[get_color(h)] == cols["red"]:
        return o * (-math.exp(0.05 * (h-300)) + 1) * 1/14 * poisson(7, 90, 1/23, 0)(h -100 - 12)
    elif cols[get_color(h)] == cols["blue"]:
        return o * 1/71 * poisson(1.7, 230, 1/23, 0)(h - 65 - 12)
    else:     
        return o * (math.exp(-0.15* (h-115)) + 1) * 5/114 * poisson(4, 115, 1/23, 0)(h - 5 - 12)

class Particle:
    def __init__(self, pos, L):
        self.pos = pos
        self.initial_pos = pos
        self.t = 0 # opacity 0.5, radius 1
        self.shape = sphere(pos = vector(pos.x, pos.z, pos.y), color = cols[get_color(pos.z)], opacity = opacity(pos.z), radius = r)#
        self.collisions = []
        self.max_z = self.pos.z
        self.L = L

    def update_pos(self):
        self.pos.z = self.max_z - self.L * self.t
        self.shape.pos = vector(self.pos.x, self.pos.z, self.pos.y)

    def reset(self):
        self.collisions = []
        self.pos = self.initial_pos
        self.t = 0

    def scatter(self, B):
        if self.t < 1:
            P = self.pos
            t = self.t

            h = P.z
            # h = round_to_nearest(P.z, 10)

            # for i in range(len(height)):
            #     if height[i] == h:
            #         index = i
            #         break

            # try:
            #     density = normalised_total[index]
            # except UnboundLocalError:
            #     print("Height out of range")

            #alpha_d = lambda h: 3 * math.pi / 180 # math.asin(B(h).getMagnitude() / B(100).getMagnitude())

            dt = 1 / 300
            #delta_alpha = 0.015

            nu = uniform(0, 1) / total(h)

            t += dt * nu

            #P_new = P + B(h).normalize()
            P_new = P + B(h).setMagnitude(self.L * dt * nu)

            #Vt = P_new - P

            #alpha = uniform(0, alpha_d(h) - t * delta_alpha)
            #beta = uniform(0, 2 * math.pi)

            #perp = Vector(Vt.z, 0, -Vt.x).normalize()
            #Vp = Vt.rotateAboutAxis(perp, alpha)
            #Vp = Vp.rotateAboutAxis(Vt.normalize(), beta)
            #Vp = Vp.setMagnitude(self.L * dt * nu / math.cos(alpha))

            #P = P + Vp
            P = P_new

            self.pos = P
            self.t = t

            self.collisions.append(sphere(pos = vector(self.pos.x, self.pos.z, self.pos.y), color = cols[get_color(self.pos.z)], opacity = opacity(self.pos.z), radius = r))#

            self.update_pos()

            return P

        else:
            self.shape.visible = False

    def is_done(self):
        if self.t > 1:
            return True
        return False




# from vpython import *
# from random import uniform, choices
# import math
# from vector import *
# import scipy as sp
# import matplotlib.pyplot as plt

# # Define a dictionary of colours
# cols = {"red": vector(1,0.23076923076923077,0),       # 630.0 nm: rgba(100%,23.076923076923077%,0%, 1)
#         "blue": vector(0.20333333333, 0, 1),           # 427.8 nm: rgba(20.333333333333314%,0%,100%, 1)
#         "green": vector(0.737, 1, 0)}     # 557.7 nm: rgba(68.14285714285721%,100%,0%, 1)

# # Get air data
# height, _, _, PN, PO, total = sp.loadtxt("data/density_and_concentration_data.csv", skiprows = 1, delimiter = ",", unpack = True)

# normalised_total = (total / total[0])**0.125

# # NOTE: 8th root taken as ration of densities exceed 10e9

# def poisson(lm, sf, c, s):
#     return lambda x: sf * lm**(c * x + s) * math.exp(-lm) / (math.gamma(c * x + s + 1))

# def green(x):
#     return poisson(1.7, 230, 1/23, 0)(x - 100 - 12)

# def blue(x):
#     return poisson(1.7, 115, 1/23, 0)(x - 100 - 12)

# def red(x):
#     return poisson(7, 90, 1/23, 0)(x -100 - 12)

# # # DEBUGGING ONLY
# # x = np.linspace(100, 300, 100)
# # y = list(map(green, x))
# # plt.plot(x, y)
# # plt.show()


# def round_to_nearest(x, n):
#     r = int(x) % n
#     if r <= n / 2:
#         return int(x - r)
#     else:
#         return int(x + n - r)


# def get_color(h):
#     # h = round_to_nearest(h, 10)
#     # for i in range(len(height)):
#     #     if height[i] == h:
#     #         index = i
#     #         break
#     choice = ["red", "green", "blue"]
#     # weights = [PO[index], PN[index] * 2 / 3, PN[index] / 3]
#     weights = [red(h), green(h), blue(h)]
#     return choices(choice, weights)[0]

# #Characteristics
# o = 0.05       #opacity
# r = 3e-1       #radius

# def opacity(h):
#     if cols[get_color(h)] == cols["red"]:
#         return o * (-math.exp(0.1 * (h-300)) + 1) * 1/14 * poisson(7, 90, 1/23, 0)(h -100 - 12)
#     elif cols[get_color(h)] == cols["blue"]:
#         return o * 0.5 * 1/71 * poisson(1.7, 230, 1/23, 0)(h - 65 - 12)
#     else:     
#         return o * (math.exp(-0.2* (h-115)) + 1) * 5/114 * poisson(4, 115, 1/23, 0)(h - 5 - 12)


# class Particle:
#     def __init__(self, pos):
#         self.pos = pos
#         self.initial_pos = pos
#         self.t = 0 # opacity 0.5, radius 1
#         self.shape = sphere(pos = vector(pos.x, pos.z, pos.y), color = cols[get_color(pos.z)], opacity = opacity(pos.z), radius = r)#
#         self.collisions = []
#         self.max_z = self.pos.z

#     def update_pos(self, L):
#         self.pos.z = self.max_z - L * self.t
#         self.shape.pos = vector(self.pos.x, self.pos.z, self.pos.y)

#     def reset(self):
#         self.collisions = []
#         self.pos = self.initial_pos
#         self.t = 0

#     def scatter(self, B, L):
#         if self.t < 1:
#             P = self.pos
#             t = self.t

#             h = round_to_nearest(P.z, 10)

#             for i in range(len(height)):
#                 if height[i] == h:
#                     index = i
#                     break

#             try:
#                 density = normalised_total[index]
#             except UnboundLocalError:
#                 print("Height out of range. Height =", h)

#             alpha_d = lambda h: 3 * math.pi / 180 # math.asin(B(h).getMagnitude() / B(100).getMagnitude())

#             dt = 1 / 300
#             delta_alpha = 0.015

#             nu = uniform(0, 1) / density

#             t += dt * nu

#             P_new = P + B(h).normalize()

#             Vt = P_new - P

#             alpha = uniform(0, alpha_d(h) - t * delta_alpha)
#             beta = uniform(0, 2 * math.pi)

#             perp = Vector(Vt.z, 0, -Vt.x).normalize()
#             Vp = Vt.rotateAboutAxis(perp, alpha)
#             Vp = Vp.rotateAboutAxis(Vt.normalize(), beta)
#             Vp = Vp.setMagnitude(L * dt * nu / math.cos(alpha))

#             P = P + Vp
            
#             self.pos = P
#             self.t = t

#             self.collisions.append(sphere(pos = vector(self.pos.x, self.pos.z, self.pos.y), color = cols[get_color(self.pos.z)], opacity = opacity(self.pos.z), radius = r))#

#             self.update_pos(L)

#             return P

#         else:
#             self.shape.visible = False

#     def is_done(self):
#         if self.t > 1:
#             return True
#         return False
