import Config

def grid_placements(boxconfig : Config.Box,
                    stemconfigs: Config.SingleStem) : #-> List[Config.PlacedStem]

        dists = []
        for stemconfig in stemconfigs:
            diam = max(stemconfig.bottom_diameter_x,
                       stemconfig.bottom_diameter_y,
                       stemconfig.middle_diameter_x,
                       stemconfig.middle_diameter_y,
                       stemconfig.top_diameter_x,
                       stemconfig.top_diameter_y)
            dists.append(diam + stemconfig.bend * 2)

        distance = max(dists)
        #print("Distance:", distance)

        if boxconfig.width < distance:
            print("\nBox too narrow!")  #irgendwie fehler melden


        # placement coordinates
        x = -boxconfig.width + distance / 2
        y = boxconfig.depth / 2
        z = distance

        xyz_placements = []
        for stemconfig in stemconfigs:
            xyz_placements.append([x,y,z])

            # update placement
            x = x + distance
            if x > (-distance / 2):
                x = x - boxconfig.width + distance
                z = z + distance

        return xyz_placements



