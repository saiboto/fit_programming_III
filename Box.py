import math

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


def create_swing(config: Config.Box) -> int:
    """Creates a 3D object of a middle pole to test the physical properties of the stems."""

    h = config.height/4
    d1 = config.depth * 0.4
    d2 = config.depth * 0.6
    dm = config.depth * 0.5
    w = config.width

    swing_col_shape_id = p.createCollisionShape(
        shapeType=p.GEOM_MESH,
        flags=p.GEOM_MESH,
        vertices=[
            [0,d1,0],
            [0,d2,0],
            [0,dm, h],
            [-w, d1, 0],
            [-w, d2, 0],
            [-w, dm, h]]
        )

    my_base_mass = 0
    my_base_collision_shape_index = swing_col_shape_id
    my_base_visual_shape_index = -1
    my_base_position = [0,0,0]
    my_base_orientation = p.getQuaternionFromEuler([0,0,0])
    my_base_inertial_frame_position = [0,0,0]


    swing_body_id = p.createMultiBody(
        baseMass=my_base_mass,
        baseCollisionShapeIndex=my_base_collision_shape_index,
        baseVisualShapeIndex=my_base_visual_shape_index,
        basePosition=my_base_position,
        baseOrientation=my_base_orientation,
        baseInertialFramePosition=my_base_inertial_frame_position,
        baseInertialFrameOrientation=my_base_orientation,
    )

    p.changeDynamics(
        bodyUniqueId=swing_body_id,
        linkIndex=-1,  # -1 points to the base body part
        lateralFriction=0.01,
        spinningFriction=0.0,
        rollingFriction=0.0,
        restitution=1,
        linearDamping=0.1
    )

    return swing_body_id


def resize(stemconfigs, boxconfig):
    '''Adjusts the size of the bounding box.
    When using the trapezoid forwarder, it is important to have a box of sufficient size,
     because otherwise the algorithm may run into an infinite loop, when,
     due to the inclination of the shape, the polter has reached a triangular shape.'''
    total_cross_section_area = sum([stemconfig.bottom_diameter_x * stemconfig.bottom_diameter_y * math.pi / 4
                                    for stemconfig in stemconfigs])  # assumes that the bottom diameter will always be the largest
    potential_front_area = total_cross_section_area * 1.5
    side_spacing = min(boxconfig.width / 4, 2.0)
    polter_height = min(boxconfig.height, (boxconfig.width - 2 * side_spacing) / 2)
    available_front_area = (boxconfig.width - 2 * side_spacing) * polter_height - polter_height ** 2  # under the assumption of an inclination of 45 deg.

    print("potential: ", potential_front_area, "available: ", available_front_area)
    if potential_front_area > available_front_area:
        A = potential_front_area
        h = boxconfig.height
        if boxconfig.width < 8:
            if h > math.sqrt(A/3): #TODO: fix formula! The relevant variable is new_width, not the old one
                print("case11")
                new_width = math.sqrt(A/3)*8
                h = math.sqrt(A/3)
            else:
                print("case12")
                new_width = 2 * (A + h**2) / h
        else:
            if 8 + math.sqrt(16 + 16 / 3 * A) < (h + 1 ) / 4:
                print("case21")
                new_width = 8 + math.sqrt(16 + 16 / 3 * A)
                h = 4 * (8 + math.sqrt(16 + 16 / 3 * A)) - 1
            else:
                print("case22")
                new_width = (A + h**2) / h + 4
        print("new_width: ", new_width)
        return Config.Box(height= h, width= new_width, depth= boxconfig.depth)

    else:
        return boxconfig
