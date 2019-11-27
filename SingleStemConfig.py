class SingleStemConfig:
    """Contains all information necessary to create a 3d stem object
    within the physics simulation.
    """
    def __init__(self,
                 length,
                 bottom_diameter_x, bottom_diameter_y,
                 middle_diameter_x, middle_diameter_y,
                 top_diameter_x, top_diameter_y,
                 bend):
        self.length = length
        self.bottom_diameter_x = bottom_diameter_x
        self.bottom_diameter_y = bottom_diameter_y
        self.middle_diameter_x = middle_diameter_x
        self.middle_diameter_y = middle_diameter_y
        self.top_diameter_x = top_diameter_x
        self.top_diameter_y = top_diameter_y
        self.bend = bend
