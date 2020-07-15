from typing import List


# The following Classes are all incorporated in the UserInput

class Box:
    def __init__(self,
                 height = 2.0,
                 width = 4.0,
                 depth = 3.0):
        self.height = height
        self.width = width
        self.depth = depth


class MeshParameters:
    '''Defines alterable modelling parameters for the generation of the 3D-Objects '''
    def __init__(self,
                 n_sides = 20,
                 n_meshes = 10,
                 bend_function = "shifted sin"):
        self.n_sides = n_sides
        self.n_meshes = n_meshes
        self.bend_function = bend_function


class PhysicsParameters:
    """Defines alterable parameters for the stem bodys in the physics engine"""
    def __init__(self,
                 lateral_friction = 0.1,
                 spinning_friction = 0.01,
                 rolling_friction = 0.01,
                 restitution = 0.1):
        self.lateral_friction = lateral_friction
        self.spinning_friction = spinning_friction
        self.rolling_friction = rolling_friction
        self.restitution = restitution


class ForwardingParameters:
    def __init__(self,
                 forwarding_algorithm="rowwise",
                 random_turn=True):
        self.forwarding_algorithm = forwarding_algorithm
        self.random_turn = random_turn


class RandomStemGeneration:
    """Defines the information necessary for random stem generation."""

    def __init__(self,
                 num_stems: int,
                 length_mean: float,
                 length_sd: float,
                 middle_stem_diameter_mean: float,
                 middle_stem_diameter_sd: float,
                 ellipticity_sd: float,
                 stem_taper_mean: float,
                 stem_taper_sd: float,
                 bend_mean: float):
        """Parameters:

        + num_stems -- Number of stems
        + length_mean -- Mean stem length ; unit: meters
        + length_sd -- Standard deviation of stem length ; unit: meters
        + middle_stem_diameter_mean -- unit: meters
        + middle_stem_diameter_sd -- unit: meters
        + ellipticity_sd -- Standard deviation around a mean of one ;
            no unit
        + stem_taper_mean -- unit: centimeters per meter
        + stem_taper_sd -- unit: centimeters per meter
        + bend_mean -- unit: centimeters per meter
        """
        self.num_stems = num_stems
        self.length_mean = length_mean
        self.length_sd = length_sd
        self.middle_stem_diameter_mean = middle_stem_diameter_mean
        self.middle_stem_diameter_sd = middle_stem_diameter_sd
        self.ellipticity_sd = ellipticity_sd
        self.stem_taper_mean = stem_taper_mean
        self.stem_taper_sd = stem_taper_sd
        self.bend_mean = bend_mean


class UserInput:
    """ Contains all information that a user can give to the program.

    Attributes
        + num_stems -- Number of stems
        + length_mean -- Mean stem length ; unit: meters
        + length_sd -- Standard deviation of stem length ; unit: meters
        + middle_stem_diameter_mean -- unit: meters
        + middle_stem_diameter_sd -- unit: meters
        + ellipticity_sd -- Standard deviation around a mean of one ; no unit
        + stem_taper_mean -- unit: centimeters per meter
        + stem_taper_sd -- unit: centimeters per meter
        + bend_mean -- unit: centimeters per meter
    """

    def __init__(self,
                 box_extent: Box,
                 settings_name="1",
                 random_stem_generation= RandomStemGeneration(0, 0, 0, 0, 0, 0, 0, 0, 0),
                 physics_parameters= PhysicsParameters(),
                 mesh_parameters= MeshParameters(),
                 forwarding_parameters= ForwardingParameters(),
                 iterations=1,
                 stems_file_path='none'):
        self.settings_name = settings_name
        self.box_extent = box_extent
        self.random_stem_generation = random_stem_generation
        self.physics_parameters = physics_parameters
        self.mesh_parameters = mesh_parameters
        self.forwarding_parameters = forwarding_parameters
        self.iterations = iterations
        self.stems_file_path = stems_file_path


class PhysicsEngine:
    def __init__(self,
                 gravity: List[float] = None):

        if gravity is None:
            self.gravity = [0, 0, -10]
        else:
            self.gravity = gravity


class SingleStem:
    """Contains all information necessary to create a 3d stem object
    within the physics simulation.
    """
    def __init__(self,
                 length: float,
                 bottom_diameter_x: float,
                 bottom_diameter_y: float,
                 middle_diameter_x: float,
                 middle_diameter_y: float,
                 top_diameter_x: float,
                 top_diameter_y: float,
                 bend=0.0,
                 density = 1000.0,
                 linear_damping=0.0,
                 mesh_parameters = MeshParameters(),
                 physics_parameters = PhysicsParameters()):

        # stem measurements
        self.length = length
        self.bottom_diameter_x = bottom_diameter_x
        self.bottom_diameter_y = bottom_diameter_y
        self.middle_diameter_x = middle_diameter_x
        self.middle_diameter_y = middle_diameter_y
        self.top_diameter_x = top_diameter_x
        self.top_diameter_y = top_diameter_y
        self.bend = bend

        # 3d object creation stuff
        self.n_sides = mesh_parameters.n_sides
        self.n_meshes = mesh_parameters.n_meshes
        self.density = density
        self.lateral_friction = physics_parameters.lateral_friction
        self.spinning_friction = physics_parameters.spinning_friction
        self.rolling_friction = physics_parameters.rolling_friction
        self.restitution = physics_parameters.restitution
        self.linear_damping = linear_damping
        self.bend_function = mesh_parameters.bend_function
        #self.random_turn = simulation_parameters.random_turn
