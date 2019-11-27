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
        #self.faces.append([v1, v2, v3])
        self.faces.append(v1)
        self.faces.append(v2)
        self.faces.append(v3)

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
    """Create an array of n_rings (kind of) cylindrical meshes, that together form a stem.

    Keyword arguments:
    config -- StemConfig object ; tree mesh configuration
    n_sides -- int ; number of sides along the stem. Must be greater than two!
    n_rings -- int ; number of rings along the stem. Must be greater than two!
    """
    meshes = []

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
#       z = pos * config.length
        z = pos * config.length - (config.length/2)
        r = createRing(xrad, yrad, n_sides, xshift, z)
        rings.append(r)
    # until here : saved all vertices, organized in rings
    # now: write into mesh-class

    for i in range(0, n_rings):
        mesh = Mesh()
        for v in rings[i]:
            mesh.vertices.append(v)
        for v in rings[i+1]:
            mesh.vertices.append(v)

        meshes.append(mesh)

    return meshes


# my_config = StemConfig(3, 0.25, 0.2, 0.18, 0.16, 0.13, 0.13, bend=0.2)

# mesh = make_stem(my_config, 20, 10)

# writeMeshFile(mesh, "mesh.obj")
