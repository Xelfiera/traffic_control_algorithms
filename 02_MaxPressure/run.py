import time

import traci
import math
from Utils import simulation

pre_mx_pressure_index = 0
mx_pressure_index = 0

def max_pressure():
    global pre_mx_pressure_index
    global mx_pressure_index
    simulation.start()
    tl_id = traci.trafficlight.getIDList()[0]
    inc_edges = simulation.get_inc_edges()
    out_edges = simulation.get_out_edges()

    while traci.simulation.getTime() < simulation.simulation_time:
        if simulation.cur_phase_duration == 0:
            if simulation.phase_status == 'g':
                inc_veh_counts = get_inrange_vehicles(inc_edges)
                out_veh_counts = get_inrange_vehicles(out_edges)
                pressures = calc_pressures(inc_veh_counts, out_veh_counts)

                pre_mx_pressure_index = mx_pressure_index
                mx_pressure_index = 0
                mx_pressure = pressures[0]
                for i, pressure in enumerate(pressures):
                    if pressure > mx_pressure:
                        mx_pressure_index = i
                        mx_pressure = pressure

                if pre_mx_pressure_index != mx_pressure_index:
                    simulation.set_yellow_phase(tl_id)
                    simulation.cur_phase_duration = 2
                    simulation.phase_status = 'y'
                else:
                    simulation.cur_phase_duration = simulation.tmin

            elif simulation.phase_status == 'y':
                simulation.set_green_phase(tl_id, inc_edges[mx_pressure_index])
                simulation.cur_phase_duration = simulation.tmin
                simulation.phase_status = 'g'

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
        vehicles_in_range.append(len(edge_vehicles))
    return vehicles_in_range

def calc_pressures(inc, out):
    pressures = []
    for i in range(4):
        pressures.append(inc[i] - out[i])
    return pressures

if __name__ == '__main__':
    max_pressure()