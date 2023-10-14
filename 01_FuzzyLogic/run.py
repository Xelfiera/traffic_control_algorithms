import traci
import time
from Utils import simulation
from fuzzy_design import calc_edge_priority

def fuzzy_logic():
    simulation.start()
    inc_edge_ids = simulation.get_inc_edges()
    tl_light = traci.trafficlight.getIDList()[0]
    edge_priorities = [0.0, 0.0, 0.0, 0.0]

    while traci.simulation.getTime() < 7200:
        for i, edge_id in enumerate(inc_edge_ids):
            waiting_vehicles = len(traci.edge.getPendingVehicles(edge_id))
            waiting_time = traci.edge.getWaitingTime(edge_id)
            edge_priorities[i] = calc_edge_priority(edge_id, waiting_vehicles, waiting_time)

        traci.simulationStep()
        time.sleep(1)

if __name__ == '__main__':
    fuzzy_logic()