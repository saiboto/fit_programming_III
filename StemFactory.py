import Config as C
import random
import YamlUI
import TableUI


def make_configs(stem_generation):
    user_input = stem_generation

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
                                             mesh_parameters= C.MeshParameters(),
                                             physics_parameters= C.PhysicsParameters()
                                             ))

    return stem_config_list


[filename, random_stem_generation_input] = YamlUI.load_user_input('simulation_settings.yaml')

stem_configs = make_configs(random_stem_generation_input)

TableUI.writeStemList(stem_configs, ("Stems/" + filename + ".csv"))