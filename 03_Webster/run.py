import math
import time

import traci
from Utils import simulation

update_freq = 600  # webster update frequency
saturation_flow = 0.38  # saturation rate (veh/s), default: 0.38

def webster():
    simulation.start()
    tl_id = traci.trafficlight.getIDList()[0]
    inc_edges = simulation.get_inc_edges()
    pre_inrange_vehicles = None
    webster_vehicle_count = [0, 0, 0, 0]
    green_times = [0, 0, 0, 0]
    pre_phase_index = 0
    cur_phase_index = 0

    while traci.simulation.getTime() < simulation.simulation_time:
        inrange_vehicles = get_inrange_vehicles(inc_edges)
        if pre_inrange_vehicles:
            for i, lane_vehicles in enumerate(pre_inrange_vehicles):
                for vehicle in lane_vehicles:
                    if vehicle not in inrange_vehicles[i]:
                        webster_vehicle_count[i] += 1

        if traci.simulation.getTime() % update_freq == 0:
            green_times = calc_websters_green_times(webster_vehicle_count)
            webster_vehicle_count = [0, 0, 0, 0]

        if simulation.cur_phase_duration == 0:
            pre_phase_index = cur_phase_index
            edge_id = inc_edges[cur_phase_index]
            simulation.set_green_phase(tl_id, edge_id)
            simulation.cur_phase_duration = green_times[cur_phase_index] + 2

            for i in range(4):
                cur_phase_index += 1
                if cur_phase_index == 4:
                    cur_phase_index = 0
                if len(get_inrange_vehicles(inc_edges)[cur_phase_index]) > 0:
                    break

        elif simulation.cur_phase_duration == 2 and cur_phase_index != pre_phase_index:
            simulation.set_yellow_phase(tl_id)

        pre_inrange_vehicles = inrange_vehicles
        simulation.cur_phase_duration -= 1
        traci.simulationStep()

def get_inrange_vehicles(edges):
    vehicles_in_range = []
    for edge in edges:
        edge_vehicles = []
        vehicles = traci.edge.getLastStepVehicleIDs(edge)
        if len(vehicles) != 0:
            for vehicle in vehicles:
                pos = traci.vehicle.getPosition(vehicle)
                dist = math.sqrt(pos[0]**2 + pos[1]**2)
                if dist <= simulation.sub_range:
                    edge_vehicles.append(vehicle)
        vehicles_in_range.append(edge_vehicles)
    return vehicles_in_range

def calc_websters_green_times(v_counts):
    y_crits = []
    for count in v_counts:
        y_crits.append((count / update_freq) / saturation_flow)

    upper_y = sum(y_crits)
    if upper_y > 0.85:
        upper_y = 0.85
    elif upper_y == 0.0:
        upper_y = 0.01

    upper_l = 4 * 2  # 2 seconds yellow for each phases
    upper_c = int(((1.5 * upper_l) + 5) / (1 - upper_y))  # calculate webster's cycle time
    upper_g = upper_c - upper_l  # total green time for cycle

    green_times = []
    for y in y_crits:
        g_time = int((y / upper_y) * upper_g)
        if g_time < simulation.tmin:
            g_time = simulation.tmin
        green_times.append(g_time)
    return green_times

if __name__ == "__main__":
    webster()