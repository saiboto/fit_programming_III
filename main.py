import sys
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

#user_inputs = YamlUI.load_user_input('simulation_settings.yaml')
user_inputs = TableUI.load_user_inputs(sys.argv)

all_results = []

for user_input in user_inputs:
    print(user_input.settings_name)
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
    if user_input.forwarding_parameters.forwarding_algorithm in ["trapezoid", "trapezoid_freeze", "trapezoid-freeze"]:
        box_config = Box.resize(stem_configs, box_config)
    box_id = Box.Box(box_config)
    #swing_id = Box.create_swing(box_config) #for debugging and experimenting only

    my_x = -box_config.width / 2
    my_y = box_config.depth / 2
    my_z = box_config.height * 1.5
    my_placement = Stem.Placement([my_x, my_x, my_z], [-math.pi * 0.5, 0, 0])
    deposit_placement = Stem.Placement([my_x, my_y, -my_z], [-math.pi * 0.5, 0, 0])

    p.resetDebugVisualizerCamera(
        cameraDistance= box_config.height + box_config.depth / 2 + box_config.width / 2,
        cameraYaw=10,
        cameraPitch=-40,
        cameraTargetPosition=[my_x, my_y, 0]
    )

    # debug_text_id = p.addUserDebugText('', my_placement.position)
    my_stems = []
    for stem_config in stem_configs:
        my_stems.append(Stem.Stem(stem_config, placement=my_placement))

    iteration_results = TableUI.emptyIterationsTable()
    for iteration in range(user_input.iterations):
        this_forwarding = Forwarder.Forwarding(my_stems, box_config, user_input.forwarding_parameters)
        iteration_results.append([iteration + 1] + this_forwarding.return_results())
        random.shuffle(my_stems)
        print(iteration, "/", user_input.iterations, end= ', ')

    print(" ")
    resultfilename = "Results/Results" + user_input.settings_name + ".csv"
    TableUI.writeResultFile(iteration_results, resultfilename)
    all_results = all_results + [i + [user_input.settings_name] for i in iteration_results[1:]]
    p.disconnect()
resultfilename = "Results/All_Results" + str(datetime.datetime.now()) + ".csv"
all_results = TableUI.emptyIterationsTable(allresults=True) + all_results
TableUI.writeResultFile(all_results, resultfilename)