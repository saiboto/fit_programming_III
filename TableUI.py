import csv
import os

import Config
import UserInterface as UI

def load_user_inputs(filepath):  #-> List[UI.Input]
    user_inputs = []
    try:
        with open(filepath, newline='') as f:
            reader = csv.reader(f, delimiter=',', quotechar= '|')
            firstrow = True
            for row in reader:
                if firstrow:
                    header = row
                    firstrow = False
                    if not header == ["settings_id", "stem_file", "iterations_number",
                                      "pile_width", "pile_height", "pile_depth",
                                      "n_sides", "n_meshes", "lateral_friction",
                                      "spinning_friction", "rolling_friction",
                                      "restitution", "bend_function", "random_turn",
                                      "drop_algorithm"]:
                        print(header)
                        raise ValueError("Invalid header!")
                else:
                    box_extend = UI.Input.BoxExtent(float(row[3]), float(row[4]), float(row[5]))
                    settings_id = str(row[0])
                    iterations = int(row[2])
                    stems_file_path = str(row[1])
                    simulation_parameters = UI.Input.SimulationParameters(n_sides=int(row[6]),
                                                                          n_meshes=int(row[7]),
                                                                          lateral_friction=float(row[8]),
                                                                          spinning_friction=float(row[9]),
                                                                          rolling_friction=float(row[10]),
                                                                          restitution=float(row[11]),
                                                                          bend_function=str(row[12]),
                                                                          random_turn=bool(row[13]),
                                                                          drop_algorithm=str(row[14]))

                    user_inputs.append(UI.Input(box_extent=box_extend,
                                                settings_name = settings_id,
                                                simulation_parameters=simulation_parameters,
                                                iterations=iterations,
                                                stems_file_path=stems_file_path))

        return user_inputs
    except KeyError as original_exc:
        raise ValueError(
            'Reading simulation settings table not successful!'
        ) from original_exc
# Up to here, the functionality is somewhat equivalent to YamlUI.
# Now come come additional functions that are needed for table interaction
#   even if the module YamlUI is used.


def writeStemList(stem_configs, filename):
    with open(filename, 'w', newline='') as f:
        my_writer = csv.writer(f)

        my_writer.writerow(["id", "length", "bottom_diam_x", "bottom_diam_y", "middle_diam_x", "middle_diam_y",
                            "top_diam_x", "top_diam_y", "bend"])
        index = 1
        for stem_config in stem_configs:
            my_writer.writerow([index, stem_config.length, stem_config.bottom_diameter_x, stem_config.bottom_diameter_y,
                               stem_config.middle_diameter_x, stem_config.middle_diameter_y,
                               stem_config.top_diameter_x, stem_config.top_diameter_y, stem_config.bend])
            index = index + 1

def writeResultFile(results, filename):
    with open(filename, 'w', newline='') as f:
        my_writer = csv.writer(f)
        my_writer.writerows(results)


def ConfigsFromStemList(user_input):
    filepath = user_input.stems_file_path
    simulation_parameters = user_input.simulation_parameters
    stemconfigs = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter=',', quotechar= '|')
        firstrow = True
        for row in reader:
            if firstrow:
                header = row
                firstrow = False
                if not header == ["id", "length", "bottom_diam_x", "bottom_diam_y",
                                  "middle_diam_x", "middle_diam_y", "top_diam_x",
                                  "top_diam_y", "bend"]:
                    raise ValueError("Invalid header!")
            else:
                stemconfigs.append(Config.SingleStem(length = float(row[1]),
                                                 bottom_diameter_x= float(row[2]),
                                                 bottom_diameter_y= float(row[3]),
                                                 middle_diameter_x= float(row[4]),
                                                 middle_diameter_y= float(row[5]),
                                                 top_diameter_x= float(row[6]),
                                                 top_diameter_y= float(row[7]),
                                                 simulation_parameters= simulation_parameters,
                                                 bend= float(row[8])))

    return stemconfigs

def resetcwd():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
