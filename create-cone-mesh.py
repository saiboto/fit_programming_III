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

        self.faces.append([currentIndex + 1, currentIndex + 2, currentIndex + 3])
####################### END Mesh class ######################

####################### BEGIN Tree generation config class ######################
class TreeConfig:
    def __init__(self, radius1, radius2, length, sides):
        self.radius1 = radius1
        self.radius2 = radius2
        self.length = length
        self.sides = sides
####################### END Tree generation config class ######################


def makeTree(config):
    mesh = Mesh()

    makeEnd(mesh, config.sides, config.radius1, 0)
    makeEnd(mesh, config.sides, config.radius2, config.length)

    makeSides(mesh, config)

    return mesh


def makeEnd(mesh, sides, radius, z):

    angle_step = 360 / sides 

    for step in range(0, sides):
    
        deg_to_rad = math.pi / 180

        a1 = step * angle_step * deg_to_rad
        a2 = (step+1) * angle_step * deg_to_rad

        x1 = math.cos(a1) * radius
        y1 = math.sin(a1) * radius

        x2 = math.cos(a2) * radius
        y2 = math.sin(a2) * radius

        mesh.createTriangle([0,0,z], [x1,y1, z], [x2, y2, z])



def makeSides(mesh, config):

    angle_step = 360 / config.sides 

    for step in range(0, config.sides):
    
        deg_to_rad = math.pi / 180

        a1 = step * angle_step * deg_to_rad
        a2 = (step+1) * angle_step * deg_to_rad

        x1_1 = math.cos(a1) * config.radius1
        y1_1 = math.sin(a1) * config.radius1

        x2_1 = math.cos(a2) * config.radius1
        y2_1 = math.sin(a2) * config.radius1

        x1_2 = math.cos(a1) * config.radius2
        y1_2 = math.sin(a1) * config.radius2

        x2_2 = math.cos(a2) * config.radius2
        y2_2 = math.sin(a2) * config.radius2


        mesh.createTriangle([x1_1, y1_1, 0], [x2_1,y2_1, 0], [x1_2, y1_2, config.length])
        mesh.createTriangle([x2_1, y2_1, 0], [x2_2, y2_2, config.length], [x1_2,y1_2,config.length])
 

def writeMeshFile(mesh, fileName):

    with open(fileName, "w") as file:
        
        # Write vertices from list to file:
        for vertex in mesh.vertices:
            file.write("v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n")

        # Write triangles from list to file:
        for face in mesh.faces:
            file.write("f " + str(face[0] + 1) + " " + str(face[1] + 1) + " " + str(face[2] + 1) + "\n")

        file.close()



config = TreeConfig(0.5, 1, 10, 20)

mesh = makeTree(config)

writeMeshFile(mesh, "mesh.obj")



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
        x = math.cos( i * math.pi * 2 / Nsides) * Xrad + xshift
        y = math.sin( i * math.pi * 2 / Nsides) * Yrad
        r.append( [x,y,z] )
    return r


#### End of class ring ####


NSides = 20   # can be altered at will

def f(x):
    return (4 * ( -x **2  + x ))
# F is the function used to describe the bend.
# F should always range between 0 and 1 for x between 0 and 1, with f(0) = 0, f(1) = 1



def makeStem(config, Nsides, Nrings):
    mesh = Mesh()

# from here: create rings
    rings = []
    for i in range(0 , Nrings + 1):
        pos = ( i / Nrings)
        if pos < 0.5:
            xrad = (config.bottomdiam1 * ( 1 - ( 2 * pos )) + config.middiam1 * (2 * pos)) / 2
            yrad = (config.bottomdiam2 * ( 1 - ( 2 * pos )) + config.middiam2 * (2 * pos)) / 2
        else:
            xrad = (config.middiam1 * (2 - (2 * pos)) + config.topdiam1 * (2 * (pos - 0.5))) / 2
            yrad = (config.middiam2 * (2 - (2 * pos)) + config.topdiam2 * (2 * (pos - 0.5))) / 2
        xshift = f(pos) * config.bend
        z = pos * config.length
        r = createRing(xrad, yrad, Nsides, xshift, z)
        rings.append(r)
# until here : saved all vertices, organized in rings
# now: make sides

    for i in range(0 , len(rings) - 1 ):
        n = len(rings[i])
        for j in range(0 , n):
            mesh.createTriangle(rings[i][j], rings[i][(j + 1) % n], rings[i + 1][j] )
            mesh.createTriangle(rings[i][ (j + 1) % n], rings[i+1][j], rings[i+1][( j + 1) % n])
#now: make Ends
    r = rings[0]
    n = len(r)
    for j in range(0, n):
        mesh.createTriangle(r[j], r[(j + 1) % n], [f(0), 0, 0])

    r = rings[len(rings) - 1]
    n = len(r)
    for j in range(0, n):
        mesh.createTriangle(r[j], r[(j + 1) % n], [f(1), 0, config.length])
# finished making ends
    return mesh


config = StemConfig(300, 25, 20, 18, 16, 13, 13, 20)

mesh = makeStem(config, 20, 10)

writeMeshFile(mesh, "mesh.obj")






