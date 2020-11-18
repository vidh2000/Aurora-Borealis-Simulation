# Import the dependencies
from noise import pnoise2
import random
import math
import numpy as np
from vector import *
import matplotlib.pyplot as plt

# Scale factor to create folds
norm = lambda x, n: 20 * (math.exp(math.cos(2 * x)) - 0.135) / n


# Parameters:
#  - Pi: Initial point of the curve (Vector)
#  - Pf: Final point of the curve (Vector)
#  - n: Number of points per period (float)
#  - b: Number of internal layers (int)
#  - i: Index of internal layer being generated (int)
#  - phi_i: Initial sin phase for i = 1 (float)
#  - phi_f: Initial sin phase for i = b (float)
#  - w: Thickness of sheet (float)
#  - wl: Wavelenght of sin wave (float)
#  - B: Magnetic field (Vector) * Assumed to be uniform *
#  - seedx: Number needed to make sure we obtain a different wave each time (float)
#  - seedy: Number needed to make sure we obtain a different wave each frame (float)
# Additional requirements:
#  - 0 <= phi_i < 2pi
#  - 0 <= phi_f < 2pi
#  - |phi_f - phi_i| <= 1
#  - 1e3 <= w <= 10e3
#  - 5.2 <= wl / 2w <= 31.4
# Returns:
#  - P: Array of initial points to begin the simulation (np.array)
def generate_curve(Pi, Pf, n, b, i, phi_i, phi_f, w, wl, B, seedx, seedy):
    # print(f"wl is {wl}")
    # print(f"seedx is {seedx}")
    # print(f"seedy is {seedy}")

    # The function first generates the curve in another set of coordinates,
    # where the firt point (Pi') is at the origin and the wavelenght (wl) is 2pi.
    # Then, the curved is transformed with matrices to the desired axis.

    # Temporary vector from Pf to Pi to get the new starting points
    temp = Pf - Pi

    # Update Pi and Pf for our layer
    Pi = Pi + temp.rotateAboutAxis(Khat, math.pi / 2).setMagnitude(w * (i - 1) / b)
    Pf = Pf + temp.rotateAboutAxis(Khat, math.pi / 2).setMagnitude(w * (i - 1) / b)

    # Vector from Pi to Pf
    Ua = Pf - Pi
    # print(f"Ua is {Ua.toString()}")

    # Result of crossing Ua and B
    Ub = Ua ** B(3e5)
    # print(f"Ub is {Ub.toString()}")

    # Initial phase in this layer
    phi = ((phi_f - phi_i) * (i - 1) / b) + phi_i
    # print(f"phi is {phi}")

    # Angle between Ua and the x axis
    theta = math.atan2(Ua.y, Ua.x)
    # print(f"theta is {theta}")

    # Scale factors for transformations
    sf_x = wl / (2 * math.pi)
    sf_y = wl / 5 # Arbitrary
    # print(f"sf_x is {sf_x}")
    # print(f"sf_y is {sf_y}")

    # Number of wavelengths being generated
    N_wav = Ua.getMagnitude() / wl
    # print(f"N_wav is {N_wav}")

    # Number of points P being calculated
    N = round(n * N_wav)
    # print(f"N is {N}")

    # Parameter to calculate the new positions
    t = 0

    # Define the increments for the perlin noise and parameter
    ds = 4 / n
    dt = 2 * math.pi * N_wav / N
    dx = 2 * math.pi * N_wav / N
    # print(f"dt is {dt}\n")

    # Store the coordinates
    X = [0]
    Y = [2 * math.sin(-dt + phi)]

    # Generate curve in xy plane, then will transform into Ua, Ub coordinates
    while X[-1] < 2 * math.pi * N_wav:
        X.append(X[-1] + pnoise2(seedx, seedy) * norm(t + phi, n) + dx)   
        Y.append(math.sin(t + phi))
        seedx += ds
        t += dt

    # Turn into numpy arrays to accelerate process
    X = np.array(X)
    Y = np.array(Y)

    # FOR DEBUGGING PURPUSES ONLY
    # plt.plot(x, y)
    # plt.show()

    # Transform back into Ua, Ub coordinates
    # Enlarge by sf
    X *= sf_x
    Y *= sf_y

    # Change the angle to theta
    X, Y = X * math.cos(theta) - Y * math.sin(theta), X * math.sin(theta) + Y * math.cos(theta)

    # Set the origin at Pi
    X += Pi.x
    Y += Pi.y

    # Make coordinates
    P = np.column_stack([X, Y])

    # DEBUGGING ONLY
    # return P, X, Y

    # Return the calculated values for P
    return P
