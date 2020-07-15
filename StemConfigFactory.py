import Config as C
import random


def run(user_input: C.UserInput):
    stem_generation = user_input.random_stem_generation

    stem_config_list = []

    for i in range(0, stem_generation.num_stems):
        mid_diameter = random.gauss(stem_generation.middle_stem_diameter_mean,
                                    stem_generation.middle_stem_diameter_sd)
        ellipticity = random.gauss(1, stem_generation.ellipticity_sd)
        taper = random.gauss(stem_generation.stem_taper_mean, stem_generation.stem_taper_sd)

        length = random.gauss(stem_generation.length_mean, stem_generation.length_sd)

        if stem_generation.bend_mean == 0:
            bend = 0
        else:
            bend = random.expovariate(1 / (user_input.bend_mean * length)) / 100

        bottom_diameter_x = (mid_diameter + ((taper * length)/2)) / 100
        bottom_diameter_y = (bottom_diameter_x * ellipticity)
        middle_diameter_x = mid_diameter / 100
        middle_diameter_y = middle_diameter_x * ellipticity
        top_diameter_x = (mid_diameter - ((taper * length)/2)) / 100
        top_diameter_y = top_diameter_x * ellipticity

        stem_config_list.append(C.SingleStem(length,
                                             bottom_diameter_x, bottom_diameter_y,
                                             middle_diameter_x, middle_diameter_y,
                                             top_diameter_x, top_diameter_y, bend,
                                             mesh_parameters=user_input.mesh_parameters,
                                             physics_parameters= user_input.physics_parameters))

    return stem_config_list
