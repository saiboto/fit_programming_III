from typing import List


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
                 n_sides=20,
                 n_meshes=10,
                 lateral_friction=0.1,#0.5
                 spinning_friction=0.01,#0.2
                 rolling_friction=0.01,#0.1
                 restitution=0.9,#0.2
                 linear_damping=0.0):

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
        self.n_sides = n_sides
        self.n_meshes = n_meshes
        self.lateral_friction = lateral_friction
        self.spinning_friction = spinning_friction
        self.rolling_friction = rolling_friction
        self.restitution = restitution
        self.linear_damping = linear_damping


# class Polter:
#     def __init__(self,
#                  width, height):


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
                 num_stems: int,
                 length_mean: float,
                 length_sd: float,
                 middle_stem_diameter_mean: float,
                 middle_stem_diameter_sd: float,
                 ellipticity_sd: float,
                 stem_taper_mean: float,
                 stem_taper_sd: float,
                 bend_mean: float):
        self.num_stems = num_stems
        self.length_mean = length_mean
        self.length_sd = length_sd
        self.middle_stem_diameter_mean = middle_stem_diameter_mean
        self.middle_stem_diameter_sd = middle_stem_diameter_sd
        self.ellipticity_sd = ellipticity_sd
        self.stem_taper_mean = stem_taper_mean
        self.stem_taper_sd = stem_taper_sd
        self.bend_mean = bend_mean

class Box:
    def __init__(self, height = 2.0, width = 4.0, depth = 3.0):
        self.height = height
        self.width = width
        self.depth = depth


class StemFactory:
    def __init__(self,
                 ):
        pass


class PhysicsEngine:
    def __init__(self,
                 gravity: List[float] = None):

        if gravity is None:
            self.gravity = [0, 0, -10]
        else:
            self.gravity = gravity

