import math
import time
import random
import datetime

import Config as C
import Stem
import Scanner
import pybullet as p

class Forwarding:
    def __init__(self, stem_list, box_config, forwarding_parameters):
        self.stems = stem_list
        self.box_config = box_config
        self._algorithm_name = forwarding_parameters.forwarding_algorithm
        self.random_turn = forwarding_parameters.random_turn
        self.random_tailflip = forwarding_parameters.random_tailflip

        self.distances = distances(stem_list)
        self._starting_time = datetime.datetime.now()

        deposit(self.stems)

        if self._algorithm_name in ["grid", "Grid", "grid_forward", "Grid_forward"]:
            grid_forward(self)
        elif self._algorithm_name in ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]:
            rowwise_forward(self)
        elif self._algorithm_name in ["simple", "Simple", "stemwise", "stem_wise"]:
            simple_forward(self)
        elif self._algorithm_name in ["trapezoid", "spaced rowwise"]:
            space = min(box_config.width / 4, 2.0)
            rowwise_forward(self, side_spacing=space, trapezoid_sides=True)
        else:
            print("WARNING: ", self._algorithm_name, ' is not a valid forwarding algorithm name. '
            'Algorithm names include "grid", "rowwise", "trapezoid" and "simple". '
            ' For now, rowwise forwarder will be used.')
            rowwise_forward(self)


def distances(my_stems):
    ''' Determines the minimum distances for stems in the following grid_placement
    or rowwise_forward, which is needed to ensure that stems do not overlap
    each other at spawn time'''
    stemconfigs = [stem.config for stem in my_stems]

    diameters = []
    distances = []
    for stemconfig in stemconfigs:
        diam = max(stemconfig.bottom_diameter_x,
                   stemconfig.bottom_diameter_y,
                   stemconfig.middle_diameter_x,
                   stemconfig.middle_diameter_y,
                   stemconfig.top_diameter_x,
                   stemconfig.top_diameter_y)
        diameters.append(diam)
        distances.append(diam + stemconfig.bend * 2)

    return [max(distances), max(diameters)]


def grid_placements(this_forwarding: Forwarding) : #-> List[Config.PlacedStem]
        ''' Will be used for grid_forward'''
        [horizontal_distance, vertical_distance] = this_forwarding.distances
        boxconfig = this_forwarding.box_config

        if boxconfig.width < horizontal_distance:
            print("\nBox too narrow!")  #irgendwie fehler melden

        # placement coordinates
        x = -boxconfig.width + horizontal_distance / 2
        y = boxconfig.depth / 2
        z = vertical_distance

        xyz_placements = []
        for stem in this_forwarding.stems:
            xyz_placements.append([x,y,z])

            # update placement
            x = x + horizontal_distance
            if x > (-horizontal_distance / 2):
                x = x - boxconfig.width + horizontal_distance
                z = z + vertical_distance

        return xyz_placements


def grid_forward(this_forwarding: Forwarding):
    xyz_placements = grid_placements(this_forwarding)

    for stem in this_forwarding.stems:
        tailflip = 0
        if this_forwarding.random_tailflip:
            tailflip = random.randint(0,1)
        if this_forwarding.random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        placement = Stem.Placement(xyz_placements.pop(0),
                                         [math.pi * tailflip, turn_angle, 0])
        stem.forward(placement)
        stem.static(False)

    for i in range(700):
        p.stepSimulation()


def rowwise_forward(this_forwarding: Forwarding,
                    waittime = 40,
                    trapezoid_sides = False,
                    side_spacing = 0.0,):
    boxconfig = this_forwarding.box_config
    stems = this_forwarding.stems
    [horizontal_dist, vertical_dist] = this_forwarding.distances
    #print(horizontal_dist, vertical_dist)
# placement coordinates
    z = vertical_dist
    y = boxconfig.depth / 2
    trapezoid_incline = z * trapezoid_sides #* math.tan(math.pi/6) # s.u.
    x = -boxconfig.width + side_spacing + horizontal_dist / 2 + trapezoid_incline


    current_row = []
    for stem in stems:
        tailflip = 0
        if this_forwarding.random_tailflip:
            tailflip = random.randint(0,1)
        if this_forwarding.random_turn:
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
        if x > (-horizontal_dist / 2 - side_spacing - trapezoid_incline):
            x = x - boxconfig.width + horizontal_dist + 2 * side_spacing + 2 * trapezoid_incline
            for i in range(waittime):
                p.stepSimulation()
                #time.sleep(1/10) #TODO: löschen
            z = Scanner.max_height(boxconfig) + vertical_dist
            #trapezoid_incline = z * trapezoid_sides * math.tan(math.pi / 6) #TODO: Find out which factor is reasonable
            trapezoid_incline = z * trapezoid_sides
            p.addUserDebugLine([x,0,z],[(-horizontal_dist/2 - side_spacing - trapezoid_incline),0,z])
            #for the_stem in current_row:
            #    the_stem.static(True)
            current_row = []

    for i in range(15):
        if max([stem.speed()[0] for stem in stems]) > 0.2:
            print("max. stem speed: " , max([stem.speed()[0] for stem in stems]))
            for i in range(waittime):
                p.stepSimulation()
        else:
            break

def simple_forward(this_forwarding: Forwarding,
                   waittime = 100):
    boxconfig = this_forwarding.box_config

    x = -boxconfig.width / 2
    y = boxconfig.depth / 2
    z = boxconfig.height * 1.5

    for stem in this_forwarding.stems:
        tailflip = 0
        if this_forwarding.random_tailflip:
            tailflip = random.randint(0, 1)
        if this_forwarding.random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        my_placement = Stem.Placement([x, y, z], [math.pi * tailflip, turn_angle, 0])
        stem.forward(my_placement)
        stem.static(False)
        for i in range(waittime):
            p.stepSimulation()
    for i in range(waittime*2):
        p.stepSimulation()


def deposit(stems):
    '''Moves the stems below the deliminating plane, as it requires less
    computation time to move them out of the way and back, compared to
    having them disappear and reappear.'''
    z = 0
    for stem in stems:
        z -= max(abs(stem.config.bottom_diameter_y),
                 abs(stem.config.middle_diameter_y),
                 abs(stem.config.top_diameter_y)) + 0.1
        place = Stem.Placement([0,0,z], [0, 0,0])
        stem.forward(place)
        stem.static(True)


def algorithm_list():
    return (["grid", "Grid", "grid_forward", "Grid_forward"]
            + ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]
            + ["simple", "Simple", "stemwise", "stem_wise"]
            + ["trapezoid", "spaced rowwise"])