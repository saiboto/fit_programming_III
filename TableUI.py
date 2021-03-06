import csv
import os

import Config as C
from Forwarder import algorithm_list
from Stem import bend_function_names

def load_user_inputs(call_arguments):  #-> List[UI.Input]
    '''Generates a list of Input class objects,
    based on a simulation settings csv file'''
    if len(call_arguments) >= 2:
        filename = call_arguments[1]
        if filename[-4:] == ".csv":
            filepath = "Settings/" + filename
        else:
            filepath = "Settings/" + filename + ".csv"
    elif len(call_arguments) == 1:
        filepath = "Settings/Settings.csv"
    else:
        raise ValueError("No argument!?!")


    # first the table is read
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
                    box_extend = C.Box(width= float(row[3]),
                                       height=float(row[4]),
                                       depth=float(row[5]))
                    settings_id = str(row[0]).strip()
                    iterations = int(row[2])
                    stems_file_path = str(row[1])
                    mesh_parameters = C.MeshParameters(n_sides=int(row[6]),
                                                       n_meshes=int(row[7]),
                                                       bend_function=str(row[12]).strip())
                    physics_parameters = C.PhysicsParameters(lateral_friction=float(row[8]),
                                                             spinning_friction=float(row[9]),
                                                             rolling_friction=float(row[10]),
                                                             restitution=float(row[11]))
                    forwarding_parameters = C.ForwardingParameters(forwarding_algorithm=str(row[14]).strip(),
                                                                   random_turn= bool(row[13]))
                    user_inputs.append(C.UserInput(box_extent=box_extend,
                                                settings_name = settings_id,
                                                mesh_parameters= mesh_parameters,
                                                physics_parameters= physics_parameters,
                                                forwarding_parameters= forwarding_parameters,
                                                iterations=iterations,
                                                stems_file_path=stems_file_path))

        validate(user_inputs)
        user_inputs = reduce(user_inputs, call_arguments)
        return user_inputs
    except KeyError as original_exc:
        raise ValueError(
            'Reading simulation settings table not successful!'
        ) from original_exc


def validate(user_inputs):
    print("Simulation settings table was read successfully.\n"
          "Validating usability...")
    warning = False
    settings_ids = [user_input.settings_name for user_input in user_inputs]
    if (len(set(settings_ids)) != len(settings_ids)):
        print("Settings IDs are not unique!")
        warning = True

    invalid_filenames = []
    for user_input in user_inputs:
        try:
            test = ConfigsFromStemList(user_input)
        except:
            invalid_filenames.append(user_input.stems_file_path)
    if invalid_filenames != []:
        print("The following stem files could not be read successfully:\n",
              set(invalid_filenames))
        warning = True

    algorithm_names = list(set([user_input.forwarding_parameters.forwarding_algorithm
                                for user_input in user_inputs]))
    invalid_algorithm_names = []
    for name in algorithm_names:
        if not(name in algorithm_list()):
            invalid_algorithm_names.append(name)
    if invalid_algorithm_names != []:
        print("The following are no valid forwarding algorithm names:\n",
              set(invalid_algorithm_names))
        warning = True

    bendf_names = list(set([user_input.mesh_parameters.bend_function
                            for user_input in user_inputs]))
    invalid_bendf_names = []
    for name in bendf_names:
        if not(name in bend_function_names()):
            invalid_bendf_names.append(name)
    if invalid_bendf_names != []:
        print("The following are no valid bend function names:",
              set(invalid_bendf_names))
        warning = True

    if warning == True:
        input("If you want to continue in spite of the above problems, press ENTER.")
    else:
        print("Settings input table valid.")


def reduce(user_inputs, call_arguments):
    '''This function checks if any valid restriction
    to a subset of the lines of the settings table was given in the call of main.py,
    in which case it reduces the user inputs to the chosen lines'''
    if len(call_arguments) == 3:
        arg = call_arguments[2]
        new_user_inputs = [user_input for user_input in user_inputs if user_input.settings_name == arg]
        if new_user_inputs == []:
            raise ValueError(
                "Call argument is not a settings id!"
            )
    elif len(call_arguments) == 4:
        arg1 = call_arguments[2]
        arg2 = call_arguments[3]
        if all([arg in [user_input.settings_name for user_input in user_inputs]
                for arg in [arg1, arg2]]) and \
                ([user_input.settings_name for user_input in user_inputs].index(arg1) < \
                 [user_input.settings_name for user_input in user_inputs].index(arg2)):
            new_user_inputs = user_inputs
            while(new_user_inputs[0].settings_name != arg1):
                new_user_inputs.pop(0)
            while(new_user_inputs[-1].settings_name != arg2):
                new_user_inputs.pop(-1)
        else:
            raise IndexError(
                "2nd and 3rd argument must be settings IDs \nand the first must occur before the second in the settings table!"
            )
    elif len(call_arguments) in [1,2]:
        new_user_inputs = user_inputs
    else:
        raise IndexError(
            "Give one or two settings names as arguments!"
        )
    return new_user_inputs

# Up to here, the functionality is somewhat equivalent to YamlUI.
# Now come come additional functions that are needed for table interaction
#   even if the module YamlUI is used.


def writeStemList(stem_configs, filename):
    with open(filename, 'w', newline='') as f:
        my_writer = csv.writer(f)

        my_writer.writerow(["id", "length",
                            "bottom_diam_x", "bottom_diam_y",
                            "middle_diam_x", "middle_diam_y",
                            "top_diam_x", "top_diam_y",
                            "bend"])
        index = 1
        for stem_config in stem_configs:
            my_writer.writerow([index,
                                stem_config.length,
                                stem_config.bottom_diameter_x,
                                stem_config.bottom_diameter_y,
                                stem_config.middle_diameter_x,
                                stem_config.middle_diameter_y,
                                stem_config.top_diameter_x,
                                stem_config.top_diameter_y,
                                stem_config.bend])
            index = index + 1

def writeResultFile(results, filename):
    with open(filename, 'w', newline='') as f:
        my_writer = csv.writer(f)
        my_writer.writerows(results)


def ConfigsFromStemList(user_input):
    filepath = "Stems/" + user_input.stems_file_path
    print(filepath)
    stemconfigs = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        firstrow = True
        for row in reader:
            if firstrow:
                header = row
                firstrow = False
                if not header == ["id", "length",
                                  "bottom_diam_x", "bottom_diam_y",
                                  "middle_diam_x", "middle_diam_y",
                                  "top_diam_x", "top_diam_y",
                                  "bend"]:
                    raise ValueError("Invalid header!")
            else:
                stemconfigs.append(C.SingleStem(length = float(row[1]),
                                                bottom_diameter_x= float(row[2]),
                                                bottom_diameter_y= float(row[3]),
                                                middle_diameter_x= float(row[4]),
                                                middle_diameter_y= float(row[5]),
                                                top_diameter_x= float(row[6]),
                                                top_diameter_y= float(row[7]),
                                                bend= float(row[8]),
                                                mesh_parameters= user_input.mesh_parameters,
                                                physics_parameters= user_input.physics_parameters))

    return stemconfigs


def emptyIterationsTable(allresults = False):
    if allresults:
        return [["Iteration", "Out Of Box", "Dislocated(any)",
                 "Dislocated(position)", "Dislocated(angle)","Front Area",
                 "Gross Volume", "Net Volume", "Deflation Factor", "Back area",
                 "Front Face Area", "Back Face Area" , "Box overflow",
                 "Duration (sec.)", "Waiting Loops", "Duration (tics)", "Settings ID"]]
    else:
        return [["Iteration", "Out Of Box", "Dislocated(any)",
                 "Dislocated(position)", "Dislocated(angle)","Front Area",
                 "Gross Volume", "Net Volume", "Deflation Factor", "Back area",
                 "Front Face Area", "Back Face Area" , "Box overflow" ,
                 "Duration (sec.)", "Waiting Loops", "Duration (tics)"]]

def resetcwd():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
