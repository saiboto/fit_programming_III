import statistics
import time
import math

import pybullet as p


class Scan:

    def __init__(self, box_config):
        self.box_config = box_config
        [front_heights, back_heights, box_overflow] = scan (box_config)

        self.front_heights = front_heights
        self.back_heights = back_heights
        self.box_overflow = box_overflow

    def max_height(self):
        return max(self.front_heights + self.back_heights)

    def front_area(self):
        return statistics.mean(self.front_heights) * self.box_config.width

    def back_area(self):
        return statistics.mean(self.back_heights) * self.box_config.width



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

        if f_hit_fraction < 0.9:
            box_overflow = True

        polter_front_heights.append(f_hit_position[2])

        #Back ray
        x_pos += step_width /3 #TODO: löschen
        b_ray_start_position = [-x_pos, box_config.depth * 0.95, box_config.height * 10]
        b_ray_target_position = [-x_pos, box_config.depth * 0.95, 0]
        backray = p.rayTest(b_ray_start_position, b_ray_target_position)

        b_hit_fraction = backray[0][2]
        b_hit_position = backray[0][3]

        if b_hit_fraction < 0.9:
            box_overflow = True

        polter_back_heights.append(b_hit_position[2])

        x_pos += 2*step_width /3

    return [polter_front_heights, polter_back_heights, box_overflow]


def face_area(this_forwarding):
    '''
    Args:
        this_forwarding: Forwarder.Forwarding
    Returns:
        The sum of the area of the stem cross sections facing front
        and the sum of the area of the stem cross sections at the back end.
    '''
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