import traci
from Utils import simulation

def max_pressure():
    simulation.start()
    tl_id = traci.trafficlight.getIDList()[0]
    inc_edges = simulation.get_inc_edges()
    out_edges = simulation.get_out_edges()

    while traci.simulation.getTime() < simulation.simulation_time:
        pressures = calc_pressures(inc_edges, out_edges)
        simulation.set_green_phase(tl_id, inc_edges[get_max_pressure_edge(pressures)])

        traci.simulationStep()

def calc_pressures(inc_edges, out_edges):
    pressures = []
    inc_vehicles = []
    out_vehicles = []
    for i in range(4):
        inc_vehicles.append(traci.edge.getLastStepHaltingNumber(inc_edges[i]))
        out_vehicles.append(traci.edge.getLastStepVehicleNumber(out_edges[i]))
        pressures.append(inc_vehicles[i] - out_vehicles[i])
    return pressures

def get_max_pressure_edge(pressures):
    max_pressure_value = 0
    max_pressure_index = 0
    for i, pressure in enumerate(pressures):
        if pressure > max_pressure_value:
            max_pressure_value = pressure
            max_pressure_index = i
    return max_pressure_index

if __name__ == '__main__':
    max_pressure()