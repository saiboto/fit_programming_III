class SingleStem:
    """Contains all information necessary to create a 3d stem object
    within the physics simulation.
    """
    def __init__(self,
                 length: float,
                 bottom_diameter_x: float, bottom_diameter_y: float,
                 middle_diameter_x: float, middle_diameter_y: float,
                 top_diameter_x: float, top_diameter_y: float,
                 bend=0.0,
                 n_sides=20, n_meshes=10,
                 lateral_friction=0.1, spinning_friction=0.01, rolling_friction=0.01,
                 restitution=0.9, linear_damping=0.0):

        # stem measurements
        self.length = length
        self.bottom_diameter_x = bottom_diameter_x
        self.bottom_diameter_y = bottom_diameter_y
        self.middle_diameter_x = middle_diameter_x
        self.middle_diameter_y = middle_diameter_y
        self.top_diameter_x = top_diameter_x
        self.top_diameter_y = top_diameter_y
        self.bend = bend

        # 3d object creation stuff
        self.n_sides = n_sides
        self.n_meshes = n_meshes
        self.lateral_friction = lateral_friction
        self.spinning_friction = spinning_friction
        self.rolling_friction = rolling_friction
        self.restitution = restitution
        self.linear_damping = linear_damping


# class Polter:
#     def __init__(self,
#                  width, height):
