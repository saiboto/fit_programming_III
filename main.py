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

my_config = create_cone_mesh.StemConfig(3, 0.25, 0.2, 0.18, 0.16, 0.13, 0.13, bend=0.2)
my_mesh = create_cone_mesh.make_stem(my_config, 20, 10)

stem_collision_shape_id = p.createCollisionShape(
    shapeType=p.GEOM_MESH,
    flags=p.GEOM_MESH,
    vertices=my_mesh.vertices,
    # indices=my_mesh.faces
)


def create_stem_body():

    stem_body_id = p.createMultiBody(
        baseMass=1,
        baseCollisionShapeIndex=stem_collision_shape_id,
        baseVisualShapeIndex=-1,
        basePosition=stem_start_pos,
        baseOrientation=stem_start_orientation,
        baseInertialFramePosition=[0, 0, 0.2],
        baseInertialFrameOrientation=stem_start_orientation
    )

    print(stem_body_id)

    p.changeDynamics(
        bodyUniqueId=stem_body_id,
        linkIndex=-1,  # -1 points to the base body part
        lateralFriction=0.1,
        spinningFriction=0.01,
        rollingFriction=0.01,
        restitution=0.9,
        linearDamping=0.0
    )


for i in range(5000):
    if i % 480 == 0:
        create_stem_body()

    p.stepSimulation()
    time.sleep(1/240)

# cubePos, cubeOrn = p.getBasePositionAndOrientation(stem_body_id)
# print(cubePos, cubeOrn)

p.disconnect()
