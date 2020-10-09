import statistics
import time
import math

import pybullet as p


class Scanresult:

    def __init__(self, front_heights, back_heights, box_overflow = False ):
        self.front_heights = front_heights
        self.back_heights = back_heights
        self.box_overflow = box_overflow


def scan(box_config):
    polter_front_heights = []
    polter_back_heights = []
    box_overflow = False
    step_width = min(0.1, box_config.width / 100)

    x_pos = min(0.05, box_config.width / 100)

    while x_pos < box_config.width - step_width / 2:
        #front ray
        f_ray_start_position = [-x_pos, box_config.depth * 0.1, box_config.height * 10]
        f_ray_target_position = [-x_pos, box_config.depth * 0.1, 0]
        frontray = p.rayTest(f_ray_start_position, f_ray_target_position)

        f_hit_fraction = frontray[0][2]
        f_hit_position = frontray[0][3]

        if f_hit_fraction < 0.1:
            box_overflow = True

        polter_front_heights.append(f_hit_position[2])


        #Back ray
        x_pos += step_width /3 #TODO: löschen
        b_ray_start_position = [-x_pos, box_config.depth * 0.95, box_config.height * 10]
        b_ray_target_position = [-x_pos, box_config.depth * 0.95, 0]
        backray = p.rayTest(b_ray_start_position, b_ray_target_position)

        b_hit_fraction = backray[0][2]
        b_hit_position = backray[0][3]

        if b_hit_fraction < 0.1:
            box_overflow = True

        polter_back_heights.append(b_hit_position[2])
        #print(f_hit_position, b_hit_position)
        #p.addUserDebugText(".", textPosition = b_hit_position)

        x_pos += 2*step_width /3

    res = Scanresult(polter_front_heights, polter_back_heights, box_overflow)
    #print(statistics.mean(polter_front_heights), statistics.mean(polter_back_heights))
    return res

def front_area(box_config, back_area = False):
    '''Determines the approximate front area of the polter by casting vertical rays on it
    and finding their intersection with the stems. '''

    my_scan = scan(box_config)

    if my_scan.box_overflow == True:
        print("WARNING: Box overflow! Too many stems for the size of the box!")

    if back_area == False:
        area = statistics.mean(my_scan.front_heights) * box_config.width
    else:
        area = statistics.mean(my_scan.back_heights) * box_config.width
    return area

def max_height(box_config):

    my_scan = scan(box_config)
    #print('max: ',  max(my_scan.front_heights), max(my_scan.back_heights), max(my_scan.front_heights + my_scan.back_heights))
    #print(my_scan.back_heights)
    return max(my_scan.front_heights + my_scan.back_heights)

def face_area(this_forwarding):
    stems = this_forwarding.stems

    front_face_area = 0
    back_face_area = 0
    for stem in stems:
        orientation2 = (math.pi*(-0.5) < stem.angles()[2] < math.pi/2)
        orientation1 = (math.pi*(-0.5) < stem.angles()[0] < math.pi/2)
        tailflip = (orientation1 == orientation2)
        if stem.is_inside_of_the_box(this_forwarding.box_config) and tailflip: # checks if the bottom or the top of the stem are facing to the front
            front_face_area += stem.config.top_diameter_x * stem.config.top_diameter_y * math.pi / 4
            back_face_area += stem.config.bottom_diameter_x * stem.config.bottom_diameter_y * math.pi / 4
        elif stem.is_inside_of_the_box(this_forwarding.box_config) and tailflip == False:
            front_face_area += stem.config.bottom_diameter_x * stem.config.bottom_diameter_y * math.pi / 4
            back_face_area += stem.config.top_diameter_x * stem.config.top_diameter_y * math.pi / 4
    return [front_face_area, back_face_area]