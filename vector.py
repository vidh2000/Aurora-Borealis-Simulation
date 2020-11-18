import random
import math
import numpy as np

# Get pi
PI = 3.141592653589793

class Vector:
    # If two arguaments are given, set z = 0
    def __init__(self, *args):
        if len(args) > 3 or len(args) < 2:
            raise ValueError("Must pass 2 or 3 arguments but {len(args)} were given")

        self.x = args[0]
        self.y = args[1]
        self.z = 0 if len(args) == 2 else args[2]


    # If 2 argumanets are given, set z = 0
    def fromPolar(*args):
        if len(args) > 3 or len(args) < 2:
            raise ValueError("Must pass 2 or 3 arguments but {len(args)} were given")

        if len(args) == 2:
            x = args[0] * math.cos(args[1])
            y = args[0] * math.sin(args[1])
            z = 0
        else:
            x = args[0] * math.cos(args[1]) * math.sin(args[2])
            y = args[0] * math.sin(args[1]) * math.sin(args[2])
            z = args[0] * math.cos(args[2])
        return Vector(x, y, z)

    # Create a unit vector in a random direction w/ z = 0
    def random2D():
        return Vector.fromPolar(1, random.random() * 2 * PI)

    # Create a 3d unit vector in a random direction
    def random3D():
        return Vector.fromPolar(1, random.random() * 2 * PI, random.random() * PI)


    # Turn vector into printable form
    def toString(self):
        return f"Vector({self.x}, {self.y}, {self.z})"

    # Turn vector into list (ignore z component)
    def toList2D(self):
        return [self.x, self.y]

    # Turn vector into a list (include z component)
    def toList3D(self):
        return [self.x, self.y, self.z]

    # Like copy.deepcopy, make a non-related copy of vector
    def copyVector(self):
        return Vector(self.x, self.y, self.z)

    # Check if two vectors are the same
    def equals(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Round each entry of vector to int
    def roundVector(self):
        return Vector(round(self.x), round(self.y), round(self.z))

    # Set the lowest and highest magnitudes
    def constrainVector(self, lower, upper):
        prev_mag = self.getMagnitude()
        new_mag = prev_mag
        if prev_mag < lower:
            new_mag = lower
        elif upper != "infty":
            if prev_mag > upper:
                new_mag = upper
        return self.setMagnitude(new_mag)


    # Use * sign
    # If Vector * Vector => dot product
    # If Vector * scalar => scalar product
    # *** If scalar * Vector => Unsupported operant type ***
    def __mul__(self, other):
        if type(other) == Vector:
            return self.x * other.x + self.y * other.y + self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vector(x, y, z)

    # Use + sing
    # Adds two vectors
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vector(x, y, z)

    # Use - sign
    # Subtracts two vectors
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vector(x, y, z)

    # Use **
    # Cross product of two Vectors
    def __pow__(this, other):
        return Vector(this.y * other.z - this.z * other.y, this.z * other.x - this.x * other.z, this.x * other.y - this.y * other.x)


    # Get magnitude of a Vector
    def getMagnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    # Set magnitude of a Vector
    def setMagnitude(self, new_mag):
        prev = self.toPolar()
        return Vector.fromPolar(new_mag, prev[1], prev[2])

    # Set magnitude to 1
    def normalize(self):
        return self.setMagnitude(1)

    # Calculate the distance between two position Vectors
    def dist(self, other):
        return (self - other).getMagnitude()


    # Turn a Vector in cartesian coordinates to spherical polar
    def toPolar(self):
        r = self.getMagnitude()
        phi = math.atan2(self.y, self.x)
        theta = math.atan2((self.x**2 + self.y**2)**0.5, self.z)
        return (r, phi, theta)

    # Turn a Vector in cartesian coordinates to cylindrical
    def toCylindrical(self):
        rho = (self.x**2 + self.y**2)**0.5
        phi = math.atan2(self.y, self.x)
        return (rho, phi, self.z)

    # 
    def rotation_matrix_3d(axis, theta):
        rot_mat = [[math.cos(theta) + axis.x**2 * (1 - math.cos(theta)), axis.x * axis.y * (1 - math.cos(theta)) - axis.z * math.sin(theta), axis.x * axis.z * (1 - math.cos(theta)) + axis.y * math.sin(theta)], 
                   [axis.y * axis.x * (1 - math.cos(theta)) + axis.z * math.sin(theta), math.cos(theta) + axis.y**2 * (1 - math.cos(theta)), axis.y * axis.z * (1 - math.cos(theta)) - axis.x * math.sin(theta)], 
                   [axis.z * axis.x * (1 - math.cos(theta)) - axis.y * math.sin(theta), axis.z * axis.y * (1 - math.cos(theta)) + axis.x * math.sin(theta), math.cos(theta) + axis.z**2 * (1 - math.cos(theta))]]
        return rot_mat

    # Rotate a Vector an angle theta (radians) (float) about an axis (Vector)
    # IMPORTANT: axis must be normalized
    # Example: V = Ihat
    #          U = V.rotateAboutAxis(Khat, PI / 2)
    #       => U = Jhat
    def rotateAboutAxis(self, axis, theta):
        rot_mat = Vector.rotation_matrix_3d(axis, theta)
        new = np.matmul(rot_mat, self.toList3D())
        return Vector(new[0], new[1], new[2])


# Define the unit Vectors for simplicity
# Exmaple:
#       from vector import *
#       print(Ihat.toString())
#    => Vector(1, 0, 0)
Ihat = Vector(1, 0, 0)
Jhat = Vector(0, 1, 0)
Khat = Vector(0, 0, 1)

