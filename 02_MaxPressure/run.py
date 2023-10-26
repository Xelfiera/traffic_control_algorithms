import traci
from Utils import simulation

def max_pressure():
    simulation.start()
    inc_edges = simulation.get_inc_edges()
    out_edges = simulation.get_out_edges()
    # tl_id = traci.trafficlight.getIDList()[0]

    while traci.simulation.getTime() < simulation.simulation_time:
        inc_vehicle_counts, out_vehicle_counts = get_lanes_vehicle_count(inc_edges, out_edges)
        edge_pressures = calc_edge_pressures(inc_vehicle_counts, out_vehicle_counts, inc_edges, out_edges)
        max_pressure_edge_index = get_max_pressure_edge(edge_pressures)
        traci.simulationStep()

def get_lanes_vehicle_count(inc_edges, out_edges):
    inc_vehicle_counts = {}
    out_vehicle_counts = {}
    for edge in inc_edges:
        inc_vehicle_counts[edge] = traci.edge.getLastStepVehicleNumber(edge)
    for edge in out_edges:
        out_vehicle_counts[edge] = traci.edge.getLastStepVehicleNumber(edge)
    return inc_vehicle_counts, out_vehicle_counts

def calc_edge_pressures(inc_vehicles, out_vehicles, inc_edges, out_edges):
    edge_pressures = []
    for i in range(4):
        edge_pressure = inc_vehicles[inc_edges[i]] - out_vehicles[out_edges[i]]
        edge_pressures.append(edge_pressure)
    return edge_pressures

def get_max_pressure_edge(edge_pressures):
    index = 0
    mx_pressure = 0
    for i, pressure in enumerate(edge_pressures):
        if pressure > mx_pressure:
            mx_pressure = pressure
            index = i
    return index

if __name__ == '__main__':
    max_pressure()