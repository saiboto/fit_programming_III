
import time

import pybullet as p
import pybullet_data

import create_cone_mesh

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -10)
planeId = p.loadURDF("plane.urdf")

cubeStartPos = [0, 0, 4]
cubeStartOrientation = p.getQuaternionFromEuler([10, 0, 0])
# boxId = p.loadURDF("r2d2.urdf", cubeStartPos, cubeStartOrientation)

stem_collision_shape_id = p.createCollisionShape(
    shapeType=p.GEOM_MESH,
    vertices=create_cone_mesh.vertices,
    indices=create_cone_mesh.indices
)

stem_body_id = p.createMultiBody(
    baseMass=1,
    baseCollisionShapeIndex=stem_collision_shape_id,
    basePosition=cubeStartPos,
    baseOrientation=cubeStartOrientation
)

for i in range(10000):
    p.stepSimulation()
    time.sleep(1/240)

cubePos, cubeOrn = p.getBasePositionAndOrientation(stem_body_id)
print(cubePos, cubeOrn)

p.disconnect()
