import math
import time
import random

import pybullet as p
import pybullet_data

import Config
import Stem
import YamlUI
import UserInterface
import StemConfigFactory
import Box
import Scanner
import Forwarder1


user_input = YamlUI.load_user_input('simulation_settings.yaml')
user_input_validator = UserInterface.Validator(user_input=user_input)

if not user_input_validator.is_valid():
    user_input_validator.print_reasons()

stem_configs = StemConfigFactory.run(user_input.random_stem_generation)
UserInterface.writeStemList(stem_configs, "My_Stems.csv")

physicsClient = p.connect(p.GUI)  #p.GUI or p.DIRECT for non-graphical version
# necessary for using objects of pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

planeId = p.loadURDF("plane.urdf")
p.changeDynamics(bodyUniqueId=planeId, linkIndex=-1, lateralFriction=50)

p.setGravity(0, 0, -10)

box_config = Config.Box(
    height=user_input.box_extent.height,
    width=user_input.box_extent.width,
    depth=user_input.box_extent.depth
)
box_id = Box.Box(box_config)

x_placement = -box_config.width / 2
y_placement = box_config.depth / 2
z_placement = box_config.height * 1.5
my_placement = Stem.Placement([x_placement, y_placement, z_placement], [-math.pi * 0.5, 0, 0])

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

iteration_results = [["Iteration", "Out Of Box", "Front Area", "Gross Volume", "Net Volume", "Deflation Factor"]]
for iteration in range(user_input.iterations):

    xyz_placements = Forwarder1.grid_placements(box_config, stem_configs)

    for stem in my_stems:
        placement = Stem.Placement(xyz_placements.pop(0),
                                         [0, 0, 0])
        stem.forward(placement)

            #time.sleep(1/240)
    for i in range(500):
        p.stepSimulation()
     #   if i % 100 == 0:
     #       print("..",i)

        # maybe change the following 3 lines to a different form of output:
    front_area = Scanner.front_area(box_config)
    net_volume = sum([stem.volume if stem.isInsideOfTheBox(box_config) else 0 for stem in my_stems])
    gross_volume = front_area * box_config.depth
    out_of_box = [stem.isInsideOfTheBox(box_config) for stem in my_stems].count(False)
    if(front_area>0):
        deflationfactor = net_volume /(front_area * box_config.depth)
    else:
        deflationfactor = "DivBy0Error"
    #print("Front area: ", front_area, '\nGross volume: ',gross_volume , '\nNet volume: ', net_volume,
    #      '\nDeflation factor:', deflationfactor, "\nStems outside of the box: ", out_of_box)
    iteration_results.append([iteration + 1, out_of_box, front_area, net_volume, gross_volume, deflationfactor])
    print(iteration)

    random.shuffle(my_stems)


UserInterface.writeResultFile(iteration_results, "Resulting_Measurements.csv")
p.disconnect()

