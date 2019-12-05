import Config
import random


def run(config: Config.UserInput):

    stem_config_list = []

    for i in range(0, config.num_stems):
        mid_diameter = random.gauss(config.middle_stem_diameter_mean,
                                    config.middle_stem_diameter_sd)
        ellipticity = random.gauss(1, config.ellipticity_sd)
        taper = random.gauss(config.stem_taper_mean,
                             config.stem_taper_sd)

        length = random.gauss(config.length_mean, config.length_sd)
        bend = random.expovariate(1 / (config.bend_mean * length))

        bottom_diameter_x = mid_diameter + (2/(taper * length))
        bottom_diameter_y = bottom_diameter_x * ellipticity
        middle_diameter_x = mid_diameter
        middle_diameter_y = middle_diameter_x * ellipticity
        top_diameter_x = mid_diameter - (2/(taper * length))
        top_diameter_y = top_diameter_x * ellipticity

        stem_config_list.append(
            Config.SingleStem(length,
                              bottom_diameter_x, bottom_diameter_y,
                              middle_diameter_x, middle_diameter_y,
                              top_diameter_x, top_diameter_y,
                              bend))

    return stem_config_list
