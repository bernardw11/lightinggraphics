import math
from display import *


  # IMPORANT NOTE

  # Ambient light is represeneted by a color value

  # Point light sources are 2D arrays of doubles.
  #      - The fist index (LOCATION) represents the vector to the light.
  #      - The second index (COLOR) represents the color.

  # Reflection constants (ka, kd, ks) are represened as arrays of
  # doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 10

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(light[LOCATION])
    normalize(view)
    color = []
    a = calculate_ambient(ambient, areflect)
    d = calculate_diffuse(light, dreflect, normal)
    s = calculate_specular(light, sreflect, view, normal)
    for i in range(3):
        color.append(int(a[i] + d[i] + s[i]))
    limit_color(color)
    return color

def calculate_ambient(alight, areflect):
    a = []
    for i in range(3):
        a.append(alight[i] * areflect[i])
    return a

def calculate_diffuse(light, dreflect, normal):
    d = []
    dot = dot_product(normal, light[LOCATION])
    if dot < 0:
        dot = 0
    for i in range(3):
        d.append(light[1][i] * dreflect[i] * dot)
    return d

def calculate_specular(light, sreflect, view, normal):
    s = []
    dot = dot_product(normal, light[LOCATION])
    for i in range(3):
        normal[i] *= (dot * 2)
        normal[i] -= float(light[0][i])
    viewdot = dot_product(normal, view)
    if viewdot < 0:
        viewdot = 0
    dissipate = viewdot ** SPECULAR_EXP
    for i in range(3):
        s.append(light[1][i] * sreflect[i] * dissipate)
    return s

def limit_color(color):
    for i in range(3):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt( vector[0] * vector[0] +
                           vector[1] * vector[1] +
                           vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude

#Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
