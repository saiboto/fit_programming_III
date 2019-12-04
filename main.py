import math
import time

import pybullet as p
import pybullet_data

import Config
import Stem


physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
# necessary for using objects of pybullet_data
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -10)

planeId = p.loadURDF("plane.urdf")

# boxId = p.loadURDF("r2d2.urdf", stem_start_position, stem_start_orientation)
# boxId = p.loadURDF("random_urdfs/000/000.urdf", stem_start_position, stem_start_orientation)

# my_config = create_cone_mesh.StemConfig(3, 0.25, 0.2, 0.18, 0.16, 0.13, 0.13, bend=0.2)
# meshes = create_cone_mesh.make_stem(my_config, 20, 10)

my_single_stem_config = Config.SingleStem(length=3,
                                          bottom_diameter_x=0.25,
                                          bottom_diameter_y=0.2,
                                          middle_diameter_x=0.18,
                                          middle_diameter_y=0.16,
                                          top_diameter_x=0.13,
                                          top_diameter_y=0.13,
                                          bend=0.2)

my_placement = Stem.Placement([0, 0, 2.5], [0, -math.pi * 0.5, 0])

debug_text_id = p.addUserDebugText('', my_placement.position)

my_stems = []

for i in range(500000):
    if i % 200 == 0:
        my_stems.append(Stem.Stem(my_single_stem_config, my_placement))
        debug_text_id = p.addUserDebugText(
            str(my_stems[-1]._pybullet_id),
            my_placement.position,
            replaceItemUniqueId=debug_text_id)

    if i == 1150:
        p.resetBasePositionAndOrientation(my_stems[5]._pybullet_id,
                                          my_placement.position,
                                          my_placement.orientation)

    p.stepSimulation()
    time.sleep(1/100)

p.disconnect()
