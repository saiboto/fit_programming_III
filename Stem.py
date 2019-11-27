import math

import SingleStemConfig


class Stem:
    def __init__(self, config: SingleStemConfig.SingleStemConfig):
        self._config = config

        def _create_ring(x_radius: float,
                         y_radius: float,
                         num_sides: int,
                         x_shift: float,
                         z: float):
            """Creates 3D-vertices that define an ellipsoidal disk.

            Keyword arguments:
            num_sides -- Number of vertices of the polygon that approximates the ellipsoid.
            x_shift -- Shifts the whole disk along the x-axis.
            z -- Z-coordinate of the disk's vertices.
            """
            r = []
            for i in range(0, num_sides):
                x = math.cos(i * math.pi * 2 / num_sides) * x_radius + x_shift
                y = math.sin(i * math.pi * 2 / num_sides) * y_radius
                r.append([x, y, z])
            return r

        def _bend_function(x: float) -> float:
            """Describes the bend of the stem.

            This should always be a function that returns values between 0 and
            1 for inputs between 0 and 1.
            """
            return 4 * (-x ** 2 + x)  # parabola
        # Try also:
        #   return (x**4-2*x**3+(5/4)*x**2-(1/4)*x)*(-64)  #polynomial double-bend
        #   return (-math.cos(x*math.pi)+1)/2  #single cos-wave
        #   return (-math.cos(x*math.pi*2)+1)/2   #double cos-wave

        def _make_stem(config: SingleStemConfig.SingleStemConfig,
                       n_sides: int,
                       n_meshes: int):
            """Create an array of n_meshes near cylindrical meshes, that
            together form a stem.

            Keyword arguments:
            config -- tree mesh configuration
            n_sides -- number of sides around each mesh. Must be greater than two!
            n_meshes -- number of meshes that form the stem. Must be greater than one!
            """

            # from here: create rings
            rings = []
            for i in range(0, n_meshes + 1):

                # The current ring's position along the stem between 0 and 1
                pos = (i / n_meshes)

                if pos < 0.5:  # before middle diameter
                    x_radius = (config.bottom_diameter_x * (1 - (2 * pos)) +
                                config.middle_diameter_x * (2 * pos)) / 2
                    y_radius = (config.bottom_diameter_y * (1 - (2 * pos)) +
                                config.middle_diameter_y * (2 * pos)) / 2
                else:  # after middle diameter
                    x_radius = (config.middle_diameter_x * (2 - (2 * pos)) +
                                config.top_diameter_x * (2 * (pos - 0.5))) / 2
                    y_radius = (config.middle_diameter_y * (2 - (2 * pos)) +
                                config.top_diameter_y * (2 * (pos - 0.5))) / 2

                x_shift = _bend_function(pos) * config.bend
                #       z = pos * config.length
                z = pos * config.length - (config.length / 2)
                r = _create_ring(x_radius, y_radius, n_sides, x_shift, z)
                rings.append(r)
            # until here: saved all vertices, organized in rings

            meshes = []
            for i in range(0, n_meshes):

                mesh = []
                for v in rings[i]:
                    mesh.append(v)
                for v in rings[i + 1]:
                    mesh.append(v)

                meshes.append(mesh)

            return meshes
