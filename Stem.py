from typing import List
import math

import pybullet as p

import Config


class Placement:
    def __init__(self, position: List[float], orientation: List[float]):
        """Creates an object that contains my_placement information.

        orientation -- rotations of multiples of pi around the x, y, and z axis
        in that order.
        """
        self.position = position
        self.orientation = p.getQuaternionFromEuler(orientation)


class Stem:
    def __init__(self, config: Config.SingleStem, placement: Placement):
        self._config = config

        meshes = _make_stem(self._config)
        self._pybullet_id = _create_stem_body(meshes, self._config, placement)


def _create_ring(x_radius: float,
                 y_radius: float,
                 num_sides: int,
                 x_shift: float,
                 z: float):
    """Creates 3D-vertices that define an ellipsoidal disk.

    Keyword arguments:
    num_sides -- Number of vertices of the polygon that approximates the ellipsoid.
    x_shift -- Shifts the whole disk along the x-axis.
    z -- Z-coordinate of the disk's vertices.
    """
    r = []
    for i in range(0, num_sides):
        x = math.cos(i * math.pi * 2 / num_sides) * x_radius + x_shift
        y = math.sin(i * math.pi * 2 / num_sides) * y_radius
        r.append([x, y, z])
    return r


def _bend_function(x: float) -> float:
    """Describes the bend of the stem.

    This should always be a function that returns values between 0 and
    1 for inputs between 0 and 1.
    """
    return 4 * (-x ** 2 + x)  # parabola

    # Try also:
    #   return (x**4-2*x**3+(5/4)*x**2-(1/4)*x)*(-64)  #polynomial double-bend
    #   return (-math.cos(x*math.pi)+1)/2  #single cos-wave
    #   return (-math.cos(x*math.pi*2)+1)/2   #double cos-wave


def _make_stem(config: Config.SingleStem) -> List[List[List[float]]]:
    """Create an array of n_meshes near cylindrical meshes, that
    together form a stem.

    Keyword arguments:
    config -- tree mesh configuration
    """

    # from here: create rings
    rings = []
    for i in range(0, config.n_meshes + 1):

        # The current ring's position along the stem between 0 and 1
        pos = (i / config.n_meshes)

        if pos < 0.5:  # before middle diameter
            x_radius = (config.bottom_diameter_x * (1 - (2 * pos)) +
                        config.middle_diameter_x * (2 * pos)) / 2
            y_radius = (config.bottom_diameter_y * (1 - (2 * pos)) +
                        config.middle_diameter_y * (2 * pos)) / 2
        else:  # after middle diameter
            x_radius = (config.middle_diameter_x * (2 - (2 * pos)) +
                        config.top_diameter_x * (2 * (pos - 0.5))) / 2
            y_radius = (config.middle_diameter_y * (2 - (2 * pos)) +
                        config.top_diameter_y * (2 * (pos - 0.5))) / 2

        x_shift = _bend_function(pos) * config.bend
        #       z = pos * config.length
        z = pos * config.length - (config.length / 2)
        r = _create_ring(x_radius, y_radius, config.n_sides, x_shift, z)
        rings.append(r)
    # until here: saved all vertices, organized in rings

    meshes = []
    for i in range(0, config.n_meshes):

        mesh = []
        for v in rings[i]:
            mesh.append(v)
        for v in rings[i + 1]:
            mesh.append(v)

        meshes.append(mesh)

    return meshes


def _create_stem_body(meshes,
                      config: Config.SingleStem,
                      placement: Placement) -> int:
    """Creates a stem's 3D representation within pybullet."""

    stem_collision_shape_ids = []
    for mesh in meshes:
        stem_col_shape_id = p.createCollisionShape(
            shapeType=p.GEOM_MESH,
            flags=p.GEOM_MESH,
            vertices=mesh,
        )
        stem_collision_shape_ids.append(stem_col_shape_id)

    my_base_mass = 1
    my_base_collision_shape_index = stem_collision_shape_ids[0]
    my_base_visual_shape_index = -1
    my_base_position = placement.position
    my_base_orientation = placement.orientation
    my_base_inertial_frame_position = [0, 0, 0.2]

    # TODO: create stem objects that each have their own mass.
    my_link_masses = [1 for x in range(len(meshes) - 1)]
    my_link_collision_shape_indices = stem_collision_shape_ids[1:]
    my_link_visual_shape_indices = [-1 for x in range(len(meshes) - 1)]
    my_link_positions = [[0, 0, 0] for x in range(len(meshes) - 1)]
    my_link_orientations = [p.getQuaternionFromEuler([0, 0, 0]) for x in range(len(meshes) - 1)]
    my_link_parent_indices = [0 for x in range(len(meshes) - 1)]
    my_link_joint_types = [p.JOINT_FIXED for x in range(len(meshes) - 1)]
    my_link_joint_axis = [[0, 0, 0] for x in range(len(meshes) - 1)]

    stem_body_id = p.createMultiBody(
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
        bodyUniqueId=stem_body_id,
        linkIndex=-1,  # -1 points to the base body part
        lateralFriction=config.lateral_friction,
        spinningFriction=config.spinning_friction,
        rollingFriction=config.rolling_friction,
        restitution=config.restitution,
        linearDamping=config.linear_damping
    )

    return stem_body_id
