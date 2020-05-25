import statistics

import pybullet as p

def front_area(box_config):
    '''Determines the approximate front area of the polter by casting vertical rays on it
    and finding their intersection with the stems. '''

    polter_height_points =[]
    box_overflow = False
    step_width = min(0.1, box_config.width/100)

    x_pos = min(0.05, box_config.width/100)

    while x_pos < box_config.width:
        ray_start_position = [-x_pos, box_config.depth*0.1, box_config.height * 2]
        ray_target_position = [-x_pos, box_config.depth*0.1, 0]
        testray = p.rayTest(ray_start_position, ray_target_position)

        hit_fraction = testray[0][2]
        hit_position = testray[0][3]

        if hit_fraction < 0.5:
            box_overflow = True

        polter_height_points.append(hit_position[2])

        x_pos += step_width

    if box_overflow == True:
        print("WARNING: Box overflow! Too many stems for the size of the box!")

    area = statistics.mean(polter_height_points) * box_config.width

    return area

