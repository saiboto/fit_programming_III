"""Handles user input data.

Public API:
    + Validator -- Validates user input dictionaries.
    + create_user_input -- Creates a user input object from a valid dictionary.
    + Input -- Defines objects that contain complete user input data.
    + Distributor -- Overwrites any core component's default config with user
    input.
"""

import cerberus

import Config


class Input:
    """Defines the information that can be included in the user input."""

    class BoxExtent:
        """Defines the information necessary for building the stem box."""

        def __init__(self, width: float, height: float, depth: float):
            """The constructor.

            Parameters:
            -------------------------
            + width -- unit: meters
            + height -- unit: meters
            + depth -- unit: meters
            """
            self.width = width
            self.height = height
            self.depth = depth

    class SimulationParameters:
        """Defines information necessary for the simulation mechanics. """

        def __init__(self,
                     n_sides =20,
                     n_meshes = 10,
                     lateral_friction =0.5,
                     spinning_friction =0.5,
                     rolling_friction = 0.5,
                     restitution = 0.1,
                     bend_function = "sin",
                     random_turn = True,
                     drop_algorithm = "default"):

            self.n_sides = n_sides
            self.n_meshes = n_meshes
            self.lateral_friction = lateral_friction
            self.spinning_friction = spinning_friction
            self.rolling_friction = rolling_friction
            self.restitution = restitution
            self.bend_function = bend_function
            self.random_turn = random_turn
            self.drop_algorithm = drop_algorithm


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

    schema = {
        'box width': {'type': 'float', 'min': 1},
        'box height': {'type': 'float', 'min': 1},
        'box depth': {'type': 'float', 'min': 1},
        'number of stems': {'type': 'integer', 'min': 1},
        'mean stem length': {'type': 'float', 'min': 1},
        'stem length standard deviation': {'type': 'float', 'min': 0},
        'mean middle stem diameter': {'type': 'float', 'min': 1},
        'middle stem diameter standard deviation': {'type': 'float', 'min': 0},
        'ellipticity standard deviation': {'type': 'float', 'min': 0},
        'mean stem taper': {'type': 'float', 'min': 1},
        'stem taper standard deviation': {'type': 'float', 'min': 0},
        'mean bend': {'type': 'float', 'min': 1}
    }

    """Defines a data schema readable by the cerberus validation framework.
    
    The schema formulates assumptions about the user input data that can be
    validated.
    """

    def __init__(self,
                 box_extent: BoxExtent,
                 settings_name = '',
                 random_stem_generation = RandomStemGeneration(0,0,0,0,0,0,0,0,0),
                 simulation_parameters = SimulationParameters(),
                 iterations = 1,
                 stems_file_path = 'none'):

        self.settings_name=settings_name
        self.box_extent = box_extent
        self.random_stem_generation = random_stem_generation
        self.simulation_parameters = simulation_parameters
        self.iterations = iterations
        self.stems_file_path = stems_file_path


class Validator:
    """Validates user input objects according to the user input schema."""

    def __init__(self, user_input: Input):

        cerberus_validator = cerberus.Validator(Input.schema)

        box_ext = user_input.box_extent
        rand_stem = user_input.random_stem_generation

        user_input_as_dict = {
            'box width': box_ext.width,
            'box height': box_ext.height,
            'box depth': box_ext.depth,
            'number of stems': rand_stem.num_stems,
            'mean stem length': rand_stem.length_mean,
            'stem length standard deviation': rand_stem.length_sd,
            'mean middle stem diameter': rand_stem.middle_stem_diameter_mean,
            'middle stem diameter standard deviation': rand_stem.middle_stem_diameter_sd,
            'ellipticity standard deviation': rand_stem.ellipticity_sd,
            'mean stem taper': rand_stem.stem_taper_mean,
            'stem taper standard deviation': rand_stem.stem_taper_sd,
            'mean bend': rand_stem.bend_mean
        }

        self._is_valid = cerberus_validator.validate(user_input_as_dict)

        if self._is_valid:
            self._invalidity_reasons = ''
        else:
            self._invalidity_reasons = cerberus_validator.errors

    def is_valid(self) -> bool:
        return self._is_valid

    def print_reasons(self):
        """Prints reasons for invalid user input to the console."""
        print(self._invalidity_reasons)


class Distributor:
    """Overwrites any core components default config with user input."""

    def __init__(self, user_input: Input):
        self._user_input = user_input

#    def insert_user_input_into_stem_factory_config(self, into: Config.SingleStem):
        """TODO"""
#        raise NotImplementedError()


