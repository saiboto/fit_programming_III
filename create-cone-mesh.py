# -*- coding: utf-8 -*-

import math


####################### BEGIN Mesh class ######################
class Mesh:
    def __init__(self):
        self.vertices = []
        self.faces = []

    def createTriangle(self, v1, v2, v3):
        currentIndex = len(self.vertices) - 1

        self.vertices.append(v1)
        self.vertices.append(v2)
        self.vertices.append(v3)


        self.faces.append(currentIndex + 1)
        self.faces.append(currentIndex + 2)
        self.faces.append(currentIndex + 3)

    def triangleByIndex(self, v1, v2, v3):
        self.faces.append([v1, v2, v3])

####################### END Mesh class ######################


def writeMeshFile(mesh, fileName):
    with open(fileName, "w") as file:

        # Write vertices from list to file:
        for vertex in mesh.vertices:
            file.write("v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n")

        # Write triangles from list to file:
        for face in mesh.faces:
            file.write("f " + str(face[0] + 1) + " " + str(face[1] + 1) + " " + str(face[2] + 1) + "\n")

        file.close()



############## Begin stem generation config class ############### by Timon, 27.10.
# This class will do the same as the above tree config class,
# with the addition of allowing more parameters, esp. curvature and elliptic stems
class StemConfig:
    def __init__(self, length, bottomdiam1, bottomdiam2, middiam1, middiam2, topdiam1, topdiam2, bend):
        self.length = length
        self.bottomdiam1 = bottomdiam1
        self.bottomdiam2 = bottomdiam2
        self.middiam1 = middiam1
        self.middiam2 = middiam2
        self.topdiam1 = topdiam1
        self.topdiam2 = topdiam2
        self.bend = bend


################## End StemConfig Class ########################


def createRing(Xrad, Yrad, Nsides, xshift, z):
    r = []
    for i in range(0, Nsides):
        x = math.cos(i * math.pi * 2 / Nsides) * Xrad + xshift
        y = math.sin(i * math.pi * 2 / Nsides) * Yrad
        r.append([x, y, z])
    return r


#### End of class ring ####


# F is the function used to describe the bend.
# F should always range between 0 and 1 for x between 0 and 1, with f(0) = 0, f(1) = 1
def f(x):
    return (4 * (-x ** 2 + x))                  # parabola
#Try also:
#   return (x**4-2*x**3+(5/4)*x**2-(1/4)*x)*(-64)  #polynomial double-bend
#   return (-math.cos(x*math.pi)+1)/2  #single cos-wave
#   return (-math.cos(x*math.pi*2)+1)/2   #double cos-wave
#   return (sqrt(1-(x/2)^2)-cos(1/2))/(1-cos(1/2))  #- 55° circular arc


def make_stem(config, n_sides, n_rings):
    """Create a stem mesh.

    Keyword arguments:
    config -- StemConfig object ; tree mesh configuration
    n_sides -- int ; number of sides along the stem. Must be greater than two!
    n_rings -- int ; number of rings along the stem. Must be greater than two!
    """
    mesh = Mesh()

    # from here: create rings
    rings = []
    for i in range(0, n_rings + 1):
        pos = (i / n_rings)
        if pos < 0.5:
            xrad = (config.bottomdiam1 * (1 - (2 * pos)) + config.middiam1 * (2 * pos)) / 2
            yrad = (config.bottomdiam2 * (1 - (2 * pos)) + config.middiam2 * (2 * pos)) / 2
        else:
            xrad = (config.middiam1 * (2 - (2 * pos)) + config.topdiam1 * (2 * (pos - 0.5))) / 2
            yrad = (config.middiam2 * (2 - (2 * pos)) + config.topdiam2 * (2 * (pos - 0.5))) / 2
        xshift = f(pos) * config.bend
        z = pos * config.length
        r = createRing(xrad, yrad, n_sides, xshift, z)
        rings.append(r)
    # until here : saved all vertices, organized in rings
    # now: write into mesh-class

    mesh.vertices.append([f(0), 0, 0])                #The center vertex of the front face will hold index 0
    for r in rings:                                 #Now the rings vertices
        for v in r:
            mesh.vertices.append(v)
    mesh.vertices.append([f(1), 0, config.length])      #The center vertex of the back face

    #Adding triangles for:
    # -front end
    for i in range(1, n_sides + 1):
        mesh.triangleByIndex(i, (i % n_sides) + 1, 0)
    # -back end
    for i in range(1, n_sides + 1):
        mesh.triangleByIndex(n_rings * n_sides + i, n_rings * n_sides + (i % n_sides) + 1, (n_rings + 1) * n_sides + 1)
    # -sides
    for i in range(0, n_rings):
        for j in range(1, n_sides + 1):
            mesh.triangleByIndex(i * n_sides + j, (i + 1) * n_sides + j, i * n_sides + ((j % n_sides) + 1))
            mesh.triangleByIndex((i + 1) * n_sides + ((j % n_sides) + 1), (i + 1) * n_sides + j, i * n_sides + ((j % n_sides) + 1))

    return mesh


my_config = StemConfig(30, 2.5, 2.0, 1.8, 1.6, 1.3, 1.3, 20.0)

mesh = make_stem(my_config, 20, 10)

writeMeshFile(mesh, "mesh.obj")

vertices = mesh.vertices
indices = mesh.faces




