import math
import time
import random
import datetime

import Config as C
import Stem
import Scanner
import pybullet as p



class Forwarding:
    '''represents the creation of one polter,
    including letting the simulation calculate after placing the stems'''
    def step_simulation(self):
        p.stepSimulation()
        self._tics_count += 1

    def __init__(self, my_stems, box_config, forwarding_parameters):
        self.stems = my_stems
        self.box_config = box_config
        self.parameters = forwarding_parameters

        self.distances = distances(my_stems)
        self._starting_time = datetime.datetime.now()
        self._tics_count = 0

        deposit(self.stems)
        wait = choose_and_execute_forwarder(self)

        self.waited_loops = wait.now(self)

        self._finish_time = datetime.datetime.now()



    def return_results(self):
        box_config = self.box_config
        front_area = Scanner.front_area(box_config)
        net_volume = sum([stem.volume if stem.is_inside_of_the_box(box_config)
                          else 0 for stem in self.stems])
        gross_volume = front_area * box_config.depth
        out_of_box = [stem.is_inside_of_the_box(box_config)
                      for stem in self.stems].count(False)
        dislocated_any = [stem.is_dislocated(box_config) for stem in self.stems].count(True)
        dislocated_position = [stem.is_dislocated_by_position(box_config) for stem in self.stems].count(True)
        dislocated_angle = [stem.is_dislocated_by_angle() for stem in self.stems].count(True)
        if (front_area > 0):
            deflationfactor = net_volume / (front_area * box_config.depth)
        else:
            deflationfactor = "DivBy0Error"

        duration = (self._finish_time - self._starting_time).total_seconds()

        return [out_of_box, dislocated_any, dislocated_position, dislocated_angle,
                front_area, gross_volume, net_volume, deflationfactor,
                duration, self.waited_loops, self._tics_count]



class Waiting:
    '''Defines the time which the simulation is left calculating after all stems have appeared.'''
    def __init__(self,
                 min_waitingtime,
                 max_loops,
                 waitingtime_per_loop,
                 static_threshold):
        '''
        min_waitingtime: The minimum number of tics which the simulation is left to calculate, regardless of if it is still moving or not
        max_loops: The maximum number of times the simulation is waiting for the stems to come to rest, before stopping the simulation anyway
        waitingtime_per_loop: The number of tics per waiting loop. A waiting loop will only be initiated if the stems in the polter are still moving.
        static_threshold: When the maximum movement speed for any stem falls below this value, the polter will be considered motionless, and no other waiting loop will be initiated
        '''
        self.min_waitingtime = min_waitingtime
        self.max_loops = max_loops
        self.waitingtime_per_loop = waitingtime_per_loop
        self.static_threshold = static_threshold


    def now(self, fwd: Forwarding):
        for i in range(self.min_waitingtime):
            fwd.step_simulation()
        loop_count = 0
        while loop_count < self.max_loops:
            if max([stem.speed()[0] for stem in fwd.stems]) > self.static_threshold:
                for i in range(self.waitingtime_per_loop):
                    fwd.step_simulation()
                loop_count += 1
            else:
                break
        return loop_count


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

        x = -boxconfig.width + horizontal_distance / 2
        y = boxconfig.depth / 2
        z = vertical_distance

        xyz_placements = []
        for stem in this_forwarding.stems:
            xyz_placements.append([x,y,z])

            x = x + horizontal_distance
            if x > (-horizontal_distance / 2):
                x = x - boxconfig.width + horizontal_distance
                z = z + vertical_distance

        return xyz_placements


def grid_forward(this_forwarding: Forwarding):
    xyz_placements = grid_placements(this_forwarding)

    for stem in this_forwarding.stems:
        tailflip = 0
        if this_forwarding.parameters.random_tailflip:
            tailflip = random.randint(0,1)
        if this_forwarding.parameters.random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        placement = Stem.Placement(xyz_placements.pop(0),
                                   [math.pi * tailflip, turn_angle, 0])
        stem.forward(placement, tailflip)
        stem.static(False)

    return Waiting(min_waitingtime=100, max_loops=20, waitingtime_per_loop=50, static_threshold=1.5)


def rowwise_forward(this_forwarding: Forwarding,
                    waittime = 40,
                    trapezoid_sides = False,
                    side_spacing = 0.0,
                    freeze = False):
    '''this_forwarding contains the general information of the Forwarding instance
        waittime describes the number of tics between the dropping of two consecutive rows

        freeze sets all stems to static once the next row comes in'''
    boxconfig = this_forwarding.box_config
    stems = this_forwarding.stems
    [horizontal_dist, vertical_dist] = this_forwarding.distances

    z = vertical_dist
    y = boxconfig.depth / 2
    trapezoid_incline = (z - vertical_dist) * trapezoid_sides #* math.tan(math.pi/6) # s.u.
    x = -boxconfig.width + side_spacing + horizontal_dist / 2 + trapezoid_incline


    current_row = []
    for stem in stems:
        tailflip = 0
        if this_forwarding.parameters.random_tailflip:
            tailflip = random.randint(0,1)
        if this_forwarding.parameters.random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        placement = Stem.Placement([x,y,z], [math.pi * tailflip, turn_angle,0])
        stem.forward(placement, xyz_velocity = [0,0,-5], tailflip= tailflip)
        stem.static(False)

        current_row.append(stem)

        #next placement
        x = x + horizontal_dist
        #row completion:
        if x > (-horizontal_dist / 2 - side_spacing - trapezoid_incline):
            x = x - boxconfig.width + horizontal_dist + 2 * side_spacing + 2 * trapezoid_incline
            print("x: ", x, " trapezoid_incline: ", trapezoid_incline, " side spacing: ", side_spacing, " dist: ", horizontal_dist) #TODO: löschen
            for i in range(waittime):
                this_forwarding.step_simulation()

            z = Scanner.max_height(boxconfig) + vertical_dist
            #trapezoid_incline = z * trapezoid_sides * math.tan(math.pi / 6) #TODO: Find out which factor is reasonable
            trapezoid_incline = min((z - vertical_dist) * trapezoid_sides , (boxconfig.width - 2*side_spacing - 2*horizontal_dist) / 2 )
            #p.addUserDebugLine([x,0,z],[(-horizontal_dist/2 - side_spacing - trapezoid_incline),0,z])
            if freeze == True:
                for this_stem in current_row:
                    this_stem.static(True)

            current_row = []

    return Waiting(min_waitingtime=40, max_loops=15, waitingtime_per_loop=50, static_threshold=0.2)


def simple_forward(this_forwarding: Forwarding,
                   waittime = 100):
    boxconfig = this_forwarding.box_config

    x = -boxconfig.width / 2
    y = boxconfig.depth / 2
    z = boxconfig.height * 1.5

    for stem in this_forwarding.stems:
        tailflip = 0
        if this_forwarding.parameters.random_tailflip:
            tailflip = random.randint(0, 1)
        if this_forwarding.parameters.random_turn:
            turn_angle = random.random() * math.pi * 2
        else:
            turn_angle = 0
        my_placement = Stem.Placement([x, y, z], [math.pi * tailflip, turn_angle, 0])
        stem.forward(my_placement, tailflip)
        stem.static(False)
        for i in range(waittime):
            this_forwarding.step_simulation()

    return Waiting(min_waitingtime=200, max_loops=0, waitingtime_per_loop=100, static_threshold=1.0)

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


def choose_and_execute_forwarder(fwd: Forwarding):
    algorithm = fwd.parameters.forwarding_algorithm
    if algorithm in ["grid", "Grid", "grid_forward", "Grid_forward"]:
        return grid_forward(fwd)

    elif algorithm in ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]:
        return rowwise_forward(fwd)

    elif algorithm in ["simple", "Simple", "stemwise", "stem_wise"]:
        return simple_forward(fwd)

    elif algorithm in ["trapezoid", "spaced rowwise"]:
        space = min(fwd.box_config.width / 4, 2.0)
        return rowwise_forward(fwd, side_spacing=space, trapezoid_sides=True)

    elif algorithm in ["rowwise-freeze" , "rowwise_freeze"]:
        return rowwise_forward(fwd, waittime= 120, freeze = True)

    elif algorithm in ["trapezoid-freeze" , "trapezoid_freeze"]:
        space = min(fwd.box_config.width / 4, 2.0)
        return rowwise_forward(fwd, waittime= 120, side_spacing=space, trapezoid_sides=True, freeze= True)

    else:
        print("WARNING: ", algorithm, ' is not a valid forwarding algorithm name. '
        'Algorithm names include "grid", "rowwise", "trapezoid" and "simple". '
        ' For now, rowwise forwarder will be used.')
        return rowwise_forward(fwd)


def algorithm_list():
    return (["grid", "Grid", "grid_forward", "Grid_forward"]
            + ["rowwise", "row-wise", "Rowwise", "rowwise_forward"]
            + ["simple", "Simple", "stemwise", "stem_wise"]
            + ["trapezoid", "spaced rowwise"]
            + ["rowwise-freeze" , "rowwise_freeze"]
            + ["trapezoid-freeze" , "trapezoid_freeze"])