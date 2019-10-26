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


