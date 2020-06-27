import UserInterface
import Config
import random


def run(user_input: UserInterface.Input.RandomStemGeneration):

    stem_config_list = []

    for i in range(0, user_input.num_stems):
        mid_diameter = random.gauss(user_input.middle_stem_diameter_mean,
                                    user_input.middle_stem_diameter_sd)
        ellipticity = random.gauss(1, user_input.ellipticity_sd)
        taper = random.gauss(user_input.stem_taper_mean, user_input.stem_taper_sd)

        length = random.gauss(user_input.length_mean, user_input.length_sd)

        if user_input.bend_mean == 0:
            bend = 0
        else:
            bend = random.expovariate(1 / (user_input.bend_mean * length)) / 100

        bottom_diameter_x = (mid_diameter + ((taper * length)/2)) / 100
        bottom_diameter_y = (bottom_diameter_x * ellipticity)
        middle_diameter_x = mid_diameter / 100
        middle_diameter_y = middle_diameter_x * ellipticity
        top_diameter_x = (mid_diameter - ((taper * length)/2)) / 100
        top_diameter_y = top_diameter_x * ellipticity

        stem_config_list.append(Config.SingleStem(length,
                                                  bottom_diameter_x, bottom_diameter_y,
                                                  middle_diameter_x, middle_diameter_y,
                                                  top_diameter_x, top_diameter_y,
                                                  bend))

    return stem_config_list
