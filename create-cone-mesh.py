# -*- coding: utf-8 -*-

import math

vertices = []
faces = []


sides = 8
angle_step = 360 / sides 


radius1 = 0.7
radius2 = 1
length = 10

def createTriangle(v1, v2, v3, vertices, faces):

    currentIndex = len(vertices) - 1

    vertices.append(v1)
    vertices.append(v2)
    vertices.append(v3)

    faces.append([currentIndex + 1, currentIndex + 2, currentIndex + 3])
    


def writeMeshFile(vertices, faces, fileName):

    with open(fileName, "w") as file:
        
        # Write vertices from list to file:
        for vertex in vertices:
            file.write("v " + str(vertex[0]) + " " + str(vertex[1]) + " " + str(vertex[2]) + "\n")

        # Write triangles from list to file:
        for face in faces:
            file.write("f " + str(face[0] + 1) + " " + str(face[1] + 1) + " " + str(face[2] + 1) + "\n")

        file.close()


def makeEnd(radius, z, vertices, faces):

    for step in range(0, sides):
      
        deg_to_rad = math.pi / 180

        a1 = step * angle_step * deg_to_rad
        a2 = (step+1) * angle_step * deg_to_rad

        x1 = math.cos(a1) * radius
        y1 = math.sin(a1) * radius

        x2 = math.cos(a2) * radius
        y2 = math.sin(a2) * radius

        createTriangle([0,0,z], [x1,y1,z], [x2, y2, z], vertices, faces)



def makeSides(radius1, radius2, z1 , z2, vertices, faces):


    for step in range(0, sides):
      
        deg_to_rad = math.pi / 180

        a1 = step * angle_step * deg_to_rad
        a2 = (step+1) * angle_step * deg_to_rad

        x1_1 = math.cos(a1) * radius1
        y1_1 = math.sin(a1) * radius1

        x2_1 = math.cos(a2) * radius1
        y2_1 = math.sin(a2) * radius1

        x1_2 = math.cos(a1) * radius2
        y1_2 = math.sin(a1) * radius2

        x2_2 = math.cos(a2) * radius2
        y2_2 = math.sin(a2) * radius2


        createTriangle([x1_1, y1_1, z1], [x2_1,y2_1,z1], [x1_2, y1_2, z2], vertices, faces)
        createTriangle([x2_1, y2_1, z1], [x2_2, y2_2, z2], [x1_2,y1_2,z2], vertices, faces)
        



makeEnd(radius1,0,vertices,faces)

makeEnd(radius2, length, vertices, faces)

makeSides(radius1, radius2, 0, length, vertices, faces )

writeMeshFile(vertices, faces, "mesh.obj")


