import math
import time
import random

import Config
import Stem
import Scanner
import pybullet as p

def distances(stemconfigs):
    diams = []
    dists = []
    for stemconfig in stemconfigs:
        diam = max(stemconfig.bottom_diameter_x,
                   stemconfig.bottom_diameter_y,
                   stemconfig.middle_diameter_x,
                   stemconfig.middle_diameter_y,
                   stemconfig.top_diameter_x,
                   stemconfig.top_diameter_y)
        diams.append(diam)
        dists.append(diam + stemconfig.bend * 2)

    return [max(dists), max(diams)]

def grid_placements(boxconfig : Config.Box,
                    stemconfigs: Config.SingleStem) : #-> List[Config.PlacedStem]


        [horizontal_distance, vertical_distance] = distances(stemconfigs)

        if boxconfig.width < horizontal_distance:
            print("\nBox too narrow!")  #irgendwie fehler melden


        # placement coordinates
        x = -boxconfig.width + horizontal_distance / 2
        y = boxconfig.depth / 2
        z = vertical_distance

        xyz_placements = []
        for stemconfig in stemconfigs:
            xyz_placements.append([x,y,z])

            # update placement
            x = x + horizontal_distance
            if x > (-horizontal_distance / 2):
                x = x - boxconfig.width + horizontal_distance
                z = z + vertical_distance

        return xyz_placements


def grid_forward(stems: Stem.Stem,
                 box_config: Config.Box,
                 random_tailflip = True,
                 random_turn = False):
    stem_configs = [stem.config for stem in stems]
    xyz_placements = grid_placements(box_config, stem_configs)

    for stem in stems:
        tailflip = 0
        if random_tailflip:
            tailflip = random.randint(0,1)
        if random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        placement = Stem.Placement(xyz_placements.pop(0),
                                         [math.pi * tailflip, turn_angle, 0])
        stem.forward(placement)
        stem.static(False)

    for i in range(700):
        p.stepSimulation()


def rowwise_forward(stems,
                    boxconfig,
                    waittime = 40,
                    random_tailflip = True,
                    random_turn = False):
    stemconfigs = [stem.config for stem in stems]
    [horizontal_dist, vertical_dist] = distances(stemconfigs)
    print(horizontal_dist, vertical_dist)
# placement coordinates
    x = -boxconfig.width + horizontal_dist / 2
    y = boxconfig.depth / 2
    z = vertical_dist

    current_row = []
    for stem in stems:
        tailflip = 0
        if random_tailflip:
            tailflip = random.randint(0,1)
        if random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        placement = Stem.Placement([x,y,z], [math.pi * tailflip, turn_angle,0])
        stem.forward(placement, xyz_velocity = [0,0,-5])
        stem.static(False)

        current_row.append(stem)

        #next placement
        x = x + horizontal_dist
        #row completion:
        if x > (-horizontal_dist / 2):
            x = x - boxconfig.width + horizontal_dist
            for i in range(waittime):
                p.stepSimulation()
            z = Scanner.max_height(boxconfig) + vertical_dist
           # for the_stem in current_row:
            #    the_stem.static(True)
            current_row = []

    for i in range(waittime):
        p.stepSimulation()

#TODO: Einen schöneren Weg finden, dass ich nicht jedem Forwarder random_turn und random_tailflip einzeln übergeben muss, um dann immer die gleichen Rechnungen ausuführen
def simple_forward(stems,
                   boxconfig,
                   waittime = 100,
                   random_tailflip = False,
                   random_turn = False):
    x = -boxconfig.width / 2
    y = boxconfig.depth / 2
    z = boxconfig.height * 1.5

    for stem in stems:
        tailflip = 0
        if random_tailflip:
            tailflip = random.randint(0, 1)
        if random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        my_placement = Stem.Placement([x, y, z], [math.pi * tailflip, turn_angle, 0])
        stem.forward(my_placement)
        stem.static(False)
        time.sleep(2) #TODO: ggf. auskommentieren/löschen
        for i in range(waittime):
            p.stepSimulation()
    for i in range(waittime*2):
        p.stepSimulation()


def deposit(stems):
    z = 0
    for stem in stems:
        z -= max(abs(stem.config.bottom_diameter_y),
                 abs(stem.config.middle_diameter_y),
                 abs(stem.config.top_diameter_y)) + 0.1
        place = Stem.Placement([0,0,z], [0, 0,0])
        stem.forward(place)
        stem.static(True)

def work(my_stems: Stem.Stem,
         box_config: Config.Box ,
         forwarding_parameters: Config.ForwardingParameters):
    algorithm_name = forwarding_parameters.forwarding_algorithm
    random_turn = forwarding_parameters.random_turn

    deposit(my_stems)

    if algorithm_name in ["grid", "Grid", "grid_forward", "Grid_forward"]:
        grid_forward(my_stems, box_config, random_turn=random_turn)
    elif algorithm_name in ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]:
        rowwise_forward(my_stems, box_config, random_turn=random_turn)
    elif algorithm_name in ["simple", "Simple", "stemwise", "stem_wise"]:
        simple_forward(my_stems, box_config, random_turn=random_turn)
    else:
        print("WARNING: ", algorithm_name, ' is not a valid forwarding algorithm name. '
                'Algorithm names include "grid", "rowwise" and "simple". '
                ' For now, rowwise forwrder will be used.')
        rowwise_forward(my_stems, box_config, random_turn=random_turn )

def algorithm_list():
    return (["grid", "Grid", "grid_forward", "Grid_forward"]
            + ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]
            + ["simple", "Simple", "stemwise", "stem_wise"])