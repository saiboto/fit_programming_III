"""Handles user config data.

Components
    + Input -- Defines the information that can be included in the user config.
    + Validator -- Validates user config.
    + Distributor -- Overwrites any core components default config with user
        config.
"""

import typing

import Config


class Input:
    """ Defines the information that can be included in the user config."""

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
            """ Parameters:

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

    def __init__(self,
                 random_stem_generation: RandomStemGeneration):
        self.random_stem_generation = random_stem_generation


class Validator:
    """Validates user config."""

    INVALID_LESS_THAN_OR_EQUAL_ZERO = (
        'The parameter "{0}" should be greater than zero, but was {1}.\n'
    )

    INVALID_LESS_THAN_ZERO = (
        'The parameter "{0}" should be equal to or greater than zero, but was '
        '{1}.\n'
    )

    def __init__(self, user_input: Input):
        self._is_valid = True
        self._error_messages = ""

        def invalid_if_less_than_or_equal_zero(user_input_element: typing.Any,
                                               input_element_name: str):
            if user_input_element <= 0:
                self._is_valid = False
                self._error_messages +=\
                    self.INVALID_LESS_THAN_OR_EQUAL_ZERO.format(
                        input_element_name, user_input_element
                    )

        def invalid_if_less_than_zero(user_input_element: typing.Any,
                                      input_element_name: str):
            if user_input_element < 0:
                self._is_valid = False
                self._error_messages +=\
                    self.INVALID_LESS_THAN_ZERO.format(
                        input_element_name, user_input_element
                    )

        invalid_if_less_than_or_equal_zero(
            user_input.random_stem_generation.num_stems,
            'number of stems'
        )

        invalid_if_less_than_or_equal_zero(
            user_input.random_stem_generation.length_mean,
            'mean stem length'
        )
        invalid_if_less_than_zero(
            user_input.random_stem_generation.length_sd,
            'stem length standard deviation'
        )

        invalid_if_less_than_or_equal_zero(
            user_input.random_stem_generation.middle_stem_diameter_mean,
            'mean middle stem diameter'
        )
        invalid_if_less_than_zero(
            user_input.random_stem_generation.middle_stem_diameter_sd,
            'middle stem diameter standard deviation'
        )

        invalid_if_less_than_zero(
            user_input.random_stem_generation.ellipticity_sd,
            'ellipticity standard deviation'
        )

        invalid_if_less_than_or_equal_zero(
            user_input.random_stem_generation.stem_taper_mean,
            'mean stem taper'
        )
        invalid_if_less_than_zero(
            user_input.random_stem_generation.stem_taper_sd,
            'stem taper standard deviation'
        )

        invalid_if_less_than_zero(
            user_input.random_stem_generation.bend_mean,
            'mean bend of stem'
        )

    def is_valid(self) -> bool:
        return self._is_valid

    def print_reasons(self):
        """Prints reasons for invalid user config to the console."""
        print(self._error_messages)


class Distributor:
    """Overwrites any core component's default config with user input."""

    def __init__(self, user_input: Input):
        self._user_input = user_input

    def insert_user_input_into_stem_factory_config(self, into: Config.SingleStem):
        """TODO"""
        raise NotImplementedError()
