from typing import List
import math
import random

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
        self.config = config

        self._meshes = _make_stem(self.config)
        self.volume = sum([slice.volume for slice in self._meshes])
        self._pybullet_id = _create_stem_body(self._meshes, self.config, placement)
        self.center_of_mass = center_of_mass(self._meshes)
        #print(self.center_of_mass) #TODO: löschen
        self.meshes = self._meshes #TODO: löschen

    def location(self):
        return p.getBasePositionAndOrientation(self._pybullet_id)[0]

    def angle(self):
        orientation = p.getEulerFromQuaternion(p.getBasePositionAndOrientation(self._pybullet_id)[1])
        x = orientation[0] % math.pi
        y = orientation[2] % math.pi
        a = min(x, math.pi-x)
        b = min(y, math.pi-y)
        return a + b #TODO: Herausfinden, wie die richtige Formel ist, mit der man den aus zwei Rotationen resultierenden Winkel zur Z-Achse errechnet

    def is_inside_of_the_box(self, boxconfig):
        if self.location()[0] < 0 and self.location()[0] > -boxconfig.width and self.location()[2] > 0 \
            and self.location()[1] > 0 and self.location()[1] < boxconfig.depth:
            return True
        else:
            return False

    def is_dislocated(self, boxconfig):
        if self.angle() < math.pi / 4 and \
            boxconfig.depth * 0.4 < self.location()[1] < boxconfig.depth * 0.6:
            return False
        else:
            return True

    def remove(self): # currently not needed
        p.removeBody(self._pybullet_id)

    def reappear(self, placement: Placement): #currently not needed
        self._pybullet_id = _create_stem_body(self._meshes, self.config, placement)

    def static(self, bool):
        if bool == True:
            for link_index in range(-1, self.config.n_meshes):
                p.changeDynamics(bodyUniqueId=self._pybullet_id,
                                 linkIndex=link_index,
                                 mass=0)
                p.resetBaseVelocity(self._pybullet_id, [0,0,0], [0,0,0,0])
        else:
            for link_index in range(-1, self.config.n_meshes - 1):
                slice = self._meshes[link_index + 1]
                p.changeDynamics(bodyUniqueId=self._pybullet_id,
                                 linkIndex=link_index,
                                 mass=slice.volume * self.config.density)

    def deposit(self, deposit_place: Placement):
        self.forward(deposit_place)
        self.static(True)

    def fetch(self, placement: Placement):
        self.forward(placement)
        self.static(False)

    def forward(self, placement :Placement, xyz_velocity = [0,0,0], tailflip = False):
        x = placement.position[0]
        z = placement.position[2]
        if tailflip:
            y = placement.position[1] + self.center_of_mass[2]
        else:
            y = placement.position[1] - self.center_of_mass[2]
        p.resetBasePositionAndOrientation(self._pybullet_id,
                                          [x,y,z],
   #                                       placement.position,
                                          placement.orientation)
        p.resetBaseVelocity(self._pybullet_id, xyz_velocity, [0,0,0,0])

    def speed(self):
        velocity = p.getBaseVelocity(self._pybullet_id)
        linear_velocity = math.sqrt(sum([x**2 for x in velocity[0]]))
        angular_velocity = sum([abs(x) for x in velocity[1]])
        return [linear_velocity, angular_velocity]



class Ring:
    """Contains 3D-vertices that define an ellipsoidal disk.
       Keyword arguments:
       n_sides -- Number of vertices of the polygon that approximates the ellipsoid.
       x_shift -- Shifts the whole disk along the x-axis.
       z -- Z-coordinate of the disk's vertices.
       """
    def __init__(self,
                 x_radius: float,
                 y_radius: float,
                 n_sides: int,
                 x_shift: float,
                 z: float):
        self.x_radius = x_radius
        self.y_radius = y_radius
        self.n_sides = n_sides
        self.x_shift = x_shift
        self.z = z

        r = []
        for i in range(0, n_sides):
            x = math.cos(i * math.pi * 2 / n_sides) * x_radius + x_shift
            y = math.sin(i * math.pi * 2 / n_sides) * y_radius
            r.append([x, y, z])
        self.vertices = r
        self.center = [x_shift, 0, z]


class Slice:
    def __init__(self, ring1, ring2):
        self.ring1 = ring1
        self.ring2 = ring2
        self.vertices = ring1.vertices + ring2.vertices
        self.volume = (abs(ring1.z - ring2.z) * math.pi / 3 *
                       (ring1.x_radius**2 + ring1.x_radius * ring2.x_radius +
                        ring2.x_radius**2) * (ring1.y_radius / ring1.x_radius))
        # volume is only precise for slices where ellipticity is the same on
        # all rings (which is the case for randomly generated stems)
        self.midpoint = weighted_midpoint(ring1.center, ring2.center,
                                          weight1=2*ring1.x_radius*ring1.y_radius + ring2.x_radius*ring2.y_radius,
                                          weight2=2*ring2.x_radius*ring2.y_radius + ring1.x_radius*ring1.y_radius)
        # midpoint formula too, is only approximate


def _generate_bend_function(type_name = "shifted sin"):
    """Returns a one-dimensional, mathematical function that calculates the
    bend of a stem.

    The returned function's signature is:
    fun(x: float) -> float
    and it returns a y value for the passed x value.
    """

    random_element = random.random()

    def bend_function(x: float):
        if type_name == "shifted sin":
            # single cos-wave
            return (-math.cos((x + random_element) * math.pi * 2) + 1) / 2
        elif type_name == "sin":
            # cos wave without shift
            return (-math.cos(x * math.pi * 2) + 1) / 2
        elif type_name == "double sin":
            # double cos wave
            return (-math.cos(x * math.pi * 2) + 1) / 2
        elif type_name == "parabola":
            # 2nd oder polynomial
            return 4 * (-x ** 2 + x)
        elif type_name == "4th order poly":
        #   # polynomial double-bend
            return (x**4 - 2 * x**3 + (5/4) * x**2 - (1/4) * x) * (-64)
        else:
            return 0

    return bend_function

def bend_function_names():
    return ["shifted sin", "sin", "double sin", "parabola", "4th order poly"]

def _make_stem(config: Config.SingleStem) -> List[Slice]:
    """Create an array of n_meshes near cylindrical meshes, that
    together form a stem.

    Keyword arguments:
    config -- tree mesh configuration
    """

    bend_function = _generate_bend_function(config.bend_function)

    if config.bend == 0:
        config.n_meshes = 1
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

        x_shift = bend_function(x=pos) * config.bend
        z = pos * config.length - (config.length / 2)
        r = Ring(x_radius, y_radius, config.n_sides, x_shift, z)
        rings.append(r)

    slices = []
    for i in range(0, config.n_meshes):
        slices.append(Slice(rings[i], rings[i+1]))

    return slices


def _create_stem_body(slices,
                      config: Config.SingleStem,
                      placement: Placement) -> int:
    """Creates a stem's 3D representation within pybullet."""

    stem_collision_shape_ids = []
    for stem_slice in slices:
        stem_col_shape_id = p.createCollisionShape(
            shapeType=p.GEOM_MESH,
            flags=p.GEOM_MESH,
            vertices=stem_slice.vertices,
        )
        stem_collision_shape_ids.append(stem_col_shape_id)


    my_base_mass = slices[0].volume * config.density
    my_base_collision_shape_index = stem_collision_shape_ids[0]
    my_base_visual_shape_index = -1
    my_base_position = placement.position
    my_base_orientation = placement.orientation
    my_base_inertial_frame_position = center_of_mass(slices)

    my_link_masses = [stem_slice.volume * config.density for stem_slice in slices[1:]]
    my_link_collision_shape_indices = stem_collision_shape_ids[1:]
    my_link_visual_shape_indices = [-1 for x in range(len(slices) - 1)]
    my_link_positions = [[0, 0, 0] for x in range(len(slices) - 1)]
    my_link_orientations = [p.getQuaternionFromEuler([0, 0, 0]) for x in range(len(slices) - 1)]
    my_link_parent_indices = [0 for x in range(len(slices) - 1)]
    my_link_joint_types = [p.JOINT_FIXED for x in range(len(slices) - 1)]
    my_link_joint_axis = [[0, 0, 0] for x in range(len(slices) - 1)]

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


def weighted_midpoint(point1, point2, weight1=1, weight2=1):
    midpoint = []
    for i in range(min(len(point1), len(point2))):
        midpoint.append(
            (point1[i] * weight1 + point2[i] * weight2) / (weight1+weight2)
        )
    return midpoint


def center_of_mass(slices):
    center = slices[0].midpoint
    mass = slices[0].volume

    for i in range(1, len(slices)):
        center = weighted_midpoint(center, slices[i].midpoint,
                                   weight1=mass,
                                   weight2=slices[i].volume)
        mass += slices[i].volume

    return center