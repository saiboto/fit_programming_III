import math
import time

import pybullet as p
import pybullet_data

import create_cone_mesh

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
p.setGravity(0, 0, -10)
planeId = p.loadURDF("plane.urdf")

stem_start_pos = [0, 0, 4]
# Orientation is given as rotations of multiples of pi around the x, y, and z
# axis in that order.
stem_start_orientation = p.getQuaternionFromEuler([0, -math.pi * 0.5, 0])

# boxId = p.loadURDF("r2d2.urdf", stem_start_pos, stem_start_orientation)
# boxId = p.loadURDF("random_urdfs/000/000.urdf", stem_start_pos, stem_start_orientation)

stem_collision_shape_id = p.createCollisionShape(
    shapeType=p.GEOM_MESH,
    vertices=create_cone_mesh.vertices,
    indices=create_cone_mesh.indices
)

stem_body_id = p.createMultiBody(
    baseMass=1,
    baseCollisionShapeIndex=stem_collision_shape_id,
    basePosition=stem_start_pos,
    baseOrientation=stem_start_orientation,
    baseInertialFramePosition=[0, 0, 0.2],
    baseInertialFrameOrientation=stem_start_orientation
)

p.changeDynamics(
    stem_body_id,
    -1,
    lateralFriction=0.1,
    spinningFriction=0.01,
    rollingFriction=0.01,
    restitution=0.9
)

for i in range(10000):
    p.stepSimulation()
    time.sleep(1/240)

cubePos, cubeOrn = p.getBasePositionAndOrientation(stem_body_id)
print(cubePos, cubeOrn)

p.disconnect()
