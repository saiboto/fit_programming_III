import pybullet as p

import Config


class Box:
    def __init__(self, config: Config.Box):
        self._config = config
        self._pybullet_id = _create_box(self._config)


def _create_box(config: Config.Box) -> int:
    """Creates a 3D object for stem bounding box within pybullet."""


    box_left_col_shape_id = p.createCollisionShape(
        shapeType=p.GEOM_MESH,
        flags=p.GEOM_MESH,
        vertices=[
            [0,0,0],
            [0,0,config.height],
            [0,config.depth, 0],
            [0, config.depth, config.height],
            [1, 0, 0],
            [1, config.depth, 0]]
        )


    box_right_col_shape_id = p.createCollisionShape(
        shapeType=p.GEOM_MESH,
        flags=p.GEOM_MESH,
        vertices=[
            [-config.width, 0, 0],
            [-config.width, 0, config.height],
            [-config.width, config.depth, 0],
            [-config.width, config.depth, config.height],
            [-(config.width + 1), 0, 0],
            [-(config.width + 1), config.depth, 0]
        ]
    )

    my_base_mass = 0
    my_base_collision_shape_index = box_left_col_shape_id
    my_base_visual_shape_index = -1
    my_base_position = [0,0,0]
    my_base_orientation = p.getQuaternionFromEuler([0,0,0])
    my_base_inertial_frame_position = [0,0,0]

    my_link_masses = [0]
    my_link_collision_shape_indices = [box_right_col_shape_id]
    my_link_visual_shape_indices = [-1]
    my_link_positions = [[0, 0, 0]]
    my_link_orientations = [p.getQuaternionFromEuler([0, 0, 0])]
    my_link_parent_indices = [0]
    my_link_joint_types = [p.JOINT_FIXED]
    my_link_joint_axis = [[0, 0, 0]]

    box_body_id = p.createMultiBody(
        baseMass=my_base_mass,
        baseCollisionShapeIndex=my_base_collision_shape_index,
        baseVisualShapeIndex=my_base_visual_shape_index,
        basePosition=my_base_position,
        baseOrientation=my_base_orientation,
        baseInertialFramePosition=my_base_inertial_frame_position,
        baseInertialFrameOrientation=my_base_orientation,

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

    p.changeDynamics(
        bodyUniqueId=box_body_id,
        linkIndex=-1,  # -1 points to the base body part
        lateralFriction=0.01,
        spinningFriction=0.0,
        rollingFriction=0.0,
        restitution=1,
        linearDamping=0.1
    )

    return box_body_id

