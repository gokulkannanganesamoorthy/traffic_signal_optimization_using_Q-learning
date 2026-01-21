import random

def generate_route_file(file_path, max_steps, n_cars):
    """
    Generates a route file with random traffic for a simple intersection.
    Assumes standard grid network with edges: n_to_c, s_to_c, e_to_c, w_to_c
    and outgoing: c_to_n, c_to_s, c_to_e, c_to_w
    """
    with open(file_path, "w") as routes:
        routes.write("<routes>\n")
        routes.write('    <vType id="standard_car" accel="0.8" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67" guiShape="passenger"/>\n')

        # Define routes (North-South, East-West)
        routes.write('    <route id="NS" edges="n_to_c c_to_s"/>\n')
        routes.write('    <route id="SN" edges="s_to_c c_to_n"/>\n')
        routes.write('    <route id="EW" edges="e_to_c c_to_w"/>\n')
        routes.write('    <route id="WE" edges="w_to_c c_to_e"/>\n')

        for car_id in range(n_cars):
            # Randomly choose a route and departure time
            route_id = random.choice(["NS", "SN", "EW", "WE"])
            depart_time = random.randint(0, max_steps - 50) # Ensure they depart before simulation ends
            
            # Sort mainly by depart time so SUMO doesn't complain (though unsorted is allowed with --route-files if using duarouter, or simple files)
            # Actually for simple one-shot generation we can just write them. 
            # Better to store and sort.
            pass
        
        # Simpler approach: Uniform distribution of cars
        # We will generate cars with random depart times, store them, sort them, then write.
        cars = []
        for i in range(n_cars):
            route_id = random.choice(["NS", "SN", "EW", "WE"])
            depart_time = random.randint(0, max_steps)
            cars.append((depart_time, route_id))
        
        cars.sort()

        for i, (depart, route) in enumerate(cars):
            routes.write(f'    <vehicle id="veh{i}" type="standard_car" route="{route}" depart="{depart}" />\n')

        routes.write("</routes>")

if __name__ == "__main__":
    generate_route_file("simulation/routes.rou.xml", 3600, 1000)
