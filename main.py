import math
import time
import random
import datetime

import pybullet as p
import pybullet_data

import Config
import Stem
import YamlUI
import StemConfigFactory
import Box
import Scanner
import Forwarder
import TableUI

TableUI.resetcwd()

# user_inputs = YamlUI.load_user_input('simulation_settings.yaml')
user_inputs = TableUI.load_user_inputs("Settings.csv")

for user_input in user_inputs:

    # user_input_validator = UserInterface.Validator(user_input=user_input)
    # if not user_input_validator.is_valid():
    #    user_input_validator.print_reasons()

    try:
        stem_configs = TableUI.ConfigsFromStemList(user_input)
    except:
        print("No valid stem file was found at the given path.",
              "A new stem set will be generated.")
        filename = input("Please give file name:")
        stem_configs = StemConfigFactory.run(user_input)
        TableUI.writeStemList(stem_configs, (filename + ".csv"))

    physicsClient = p.connect(p.GUI)  #p.GUI or p.DIRECT for non-graphical version

    # necessary for using objects of pybullet_data
    p.setAdditionalSearchPath(pybullet_data.getDataPath())

    planeId = p.loadURDF("plane.urdf", basePosition=[-14,0,0])
    p.changeDynamics(bodyUniqueId=planeId, linkIndex=-1, lateralFriction=50)

    p.setGravity(0, 0, -10)

    box_config = user_input.box_extent
    if user_input.forwarding_parameters.forwarding_algorithm == "trapezoid":
        box_config = Box.resize(stem_configs, box_config)
    box_id = Box.Box(box_config)
    #swing_id = Box.create_swing(box_config) #for debugging and experimenting only

    x_placement = -box_config.width / 2
    y_placement = box_config.depth / 2
    z_placement = box_config.height * 1.5
    my_placement = Stem.Placement([x_placement, y_placement, z_placement], [-math.pi * 0.5, 0, 0])
    deposit_placement = Stem.Placement([x_placement, y_placement, -z_placement], [-math.pi * 0.5, 0, 0])

    p.resetDebugVisualizerCamera(
        cameraDistance= box_config.height + box_config.depth / 2 + box_config.width / 2,
                    #=box_config.height + box_config.height * box_config.width * box_config.depth / 10,
        cameraYaw=10,
        cameraPitch=-40,
        cameraTargetPosition=[x_placement, y_placement, 0]
    )

    # debug_text_id = p.addUserDebugText('', my_placement.position)

    my_stems = []
    for stem_config in stem_configs:
        my_stems.append(Stem.Stem(stem_config, placement=my_placement))
    #for stem in my_stems:                   #as I was trying to find out why unbent stems seem to have no more than 20 vertices per ring, even if specified otherwise
    #    print(stem.meshes[0].ring1.n_sides)
    #    print(stem.meshes[0].ring1.vertices)

    iteration_results = [["Iteration", "Out Of Box", "Dislocated","Front Area", "Gross Volume", "Net Volume", "Deflation Factor", "Duation (sec.)", "Waiting Loops", "Duration (tics)"]]
    for iteration in range(user_input.iterations):

        this_forwarding = Forwarder.Forwarding(my_stems, box_config, user_input.forwarding_parameters)

        iteration_results.append([iteration + 1] + this_forwarding.return_results())
        random.shuffle(my_stems)

    print(user_input.settings_name)
    resultfilename = "Results/Results" + user_input.settings_name + ".csv"
    TableUI.writeResultFile(iteration_results, resultfilename)
    p.disconnect()