import math
import time

import pybullet as p
import pybullet_data

import create_cone_mesh

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally

p.setGravity(0, 0, -10)

planeId = p.loadURDF("plane.urdf")

# boxId = p.loadURDF("r2d2.urdf", stem_start_position, stem_start_orientation)
# boxId = p.loadURDF("random_urdfs/000/000.urdf", stem_start_position, stem_start_orientation)

my_config = create_cone_mesh.StemConfig(3, 0.25, 0.2, 0.18, 0.16, 0.13, 0.13, bend=0.2)
my_meshes = create_cone_mesh.make_stem(my_config, 20, 10)

stem_collision_shape_ids = []
for mesh in my_meshes:
    stem_col_shape_id = p.createCollisionShape(
        shapeType=p.GEOM_MESH,
        flags=p.GEOM_MESH,
        vertices=mesh.vertices,
        # indices=mesh.faces
    )
    stem_collision_shape_ids.append(stem_col_shape_id)

stem_start_position = [0, 0, 4]
# Orientation is given as rotations of multiples of pi around the x, y, and z
# axis in that order.
stem_start_orientation = p.getQuaternionFromEuler([0, -math.pi * 0.5, 0])
stem_inertial_frame_position = [0, 0, 0.2]

my_base_mass = 1
my_base_collision_shape_index = stem_collision_shape_ids[0]
my_base_visual_shape_index = -1
my_base_position = [0, 0, 3]

# TODO: create stem objects that each have their own mass.
my_link_masses = [1 for x in range(len(my_meshes) - 1)]
my_link_collision_shape_indices = stem_collision_shape_ids[1:]
my_link_visual_shape_indices = [-1 for x in range(len(my_meshes) - 1)]
my_link_positions = [[0, 0, 0] for x in range(len(my_meshes) - 1)]
my_link_orientations = [p.getQuaternionFromEuler([0, 0, 0]) for x in range(len(my_meshes) - 1)]
my_link_parent_indices = [0 for x in range(len(my_meshes) - 1)]
my_link_joint_types = [p.JOINT_FIXED for x in range(len(my_meshes) - 1)]
my_link_joint_axis = [[0, 0, 0] for x in range(len(my_meshes) - 1)]


def create_stem_body():

    stem_body_id = p.createMultiBody(
        baseMass=1,
        baseCollisionShapeIndex=stem_collision_shape_ids[0],
        baseVisualShapeIndex=-1,
        basePosition=stem_start_position,
        baseOrientation=stem_start_orientation,
        baseInertialFramePosition=stem_inertial_frame_position,
        baseInertialFrameOrientation=stem_start_orientation,

        linkMasses=my_link_masses,
        linkCollisionShapeIndices=my_link_collision_shape_indices,
        linkVisualShapeIndices=my_link_visual_shape_indices,
        linkPositions=my_link_positions,
        linkOrientations=my_link_orientations,
        linkInertialFramePositions=my_link_positions,
        linkInertialFrameOrientations=my_link_orientations,
        linkParentIndices=my_link_parent_indices,
        linkJointTypes=my_link_joint_types,
        linkJointAxis=my_link_joint_axis
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


for i in range(500000):
    if i % 480 == 0:
        create_stem_body()

    p.stepSimulation()
    time.sleep(1/240)

# cubePos, cubeOrn = p.getBasePositionAndOrientation(stem_body_id)
# print(cubePos, cubeOrn)

p.disconnect()
