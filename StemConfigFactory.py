import Config
import andom


def run(input: Config.UserInput):

    stem_config_list = []

    for i in range(0, input.num_stems):
        mid_diameter = random.gauss(input.middle_stem_diameter_mean, input.middle_stem_diameter_sd)
        ellipticity = random.gauss(1, input.ellipticity_sd)
        taper = random.gauss(input.stem_taper_mean, input.stem_taper_sd)

        length = random.gauss(input.length_mean, input.length_sd)
        bend = random.expovariate(1/(input.bend_mean*length))

        bottom_diameter_x = mid_diameter + (2/(taper * length))
        bottom_diameter_y = bottom_diameter_x * ellipticity
        middle_diameter_x = mid_diameter
        middle_diameter_y = middle_diameter_x * ellipticity
        top_diameter_x = mid_diameter - (2/(taper * length))
        top_diameter_y = top_diameter_x * ellipticity

        stem_config_list.append(Config.SingleStem(length,
                                                  bottom_diameter_x, bottom_diameter_y,
                                                  middle_diameter_x, middle_diameter_y,
                                                  top_diameter_x, top_diameter_y,
                                                  bend))

    return stem_config_list
