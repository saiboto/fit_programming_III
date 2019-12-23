import math
import time

import pybullet as p
import pybullet_data

import Config
import Stem
import YamlUI
import UserInterface
import StemConfigFactory
import Box
import Scanner


user_input = YamlUI.load_user_input('simulation_settings.yaml')
user_input_validator = UserInterface.Validator(user_input=user_input)

if not user_input_validator.is_valid():
    user_input_validator.print_reasons()

stem_configs = StemConfigFactory.run(user_input.random_stem_generation)

physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
# necessary for using objects of pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -10)

planeId = p.loadURDF("plane.urdf")

box_config = Config.Box(height=1, width=1, depth=3)
box_id = Box.Box(box_config)

x_placement = -box_config.width / 2
y_placement = box_config.depth / 2
z_placement = box_config.height * 1.5
my_placement = Stem.Placement([x_placement, y_placement, z_placement], [-math.pi * 0.5, 0, 0])

debug_text_id = p.addUserDebugText('', my_placement.position)

my_stems = []
for stem_config in stem_configs:
    my_stems.append(Stem.Stem(stem_config, placement=my_placement))

    for i in range(200):
        p.stepSimulation()
        # time.sleep(1/240)

    # maybe change the following 3 lines to a different form of output:
    front_area = Scanner.front_area(box_config)
    net_volume = sum([stem.volume for stem in my_stems])
    print("Front area: ", front_area, '\nGross volume: ', front_area * box_config.depth, '\nNet volume: ', net_volume,
          '\nDeflation factor:', net_volume /(front_area * box_config.depth) )
    time.sleep(1)

#
# my_stems = []
# for i in range(500000):
#     if i % 200 == 0:
#         my_stems.append(Stem.Stem(my_single_stem_config, my_placement))
#         debug_text_id = p.addUserDebugText(
#             str(my_stems[-1]._pybullet_id),
#             my_placement.position,
#             replaceItemUniqueId=debug_text_id)
#
#     if i == 1150:
#         p.resetBasePositionAndOrientation(my_stems[5]._pybullet_id,
#                                           my_placement.position,
#                                           my_placement.orientation)
#
#     p.stepSimulation()
#     time.sleep(1/100)

p.disconnect()
