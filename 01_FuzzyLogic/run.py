import traci
from Utils import simulation
from fuzzy_design import calc_edge_priority

def fuzzy_logic():
    simulation.start()
    inc_edge_ids = simulation.get_inc_edges()
    tl_id = traci.trafficlight.getIDList()[0]

    while traci.simulation.getTime() < simulation.simulation_time:
        max_priority_edge = inc_edge_ids[get_max_priority_edge(inc_edge_ids)]
        if simulation.cur_phase_duration <= -3:
            simulation.set_green_phase(tl_id, max_priority_edge)
            simulation.cur_phase_duration = traci.edge.getLastStepHaltingNumber(max_priority_edge) * 4
        elif simulation.cur_phase_duration == 0:
            simulation.set_yellow_phase(tl_id)
        simulation.cur_phase_duration -= 1
        traci.simulationStep()

def get_max_priority_edge(inc_edge_ids):
    max_priority = 0.0
    max_priority_index = 0
    for i, edge_id in enumerate(inc_edge_ids):
        waiting_vehicles = traci.edge.getLastStepHaltingNumber(edge_id)
        waiting_time = traci.edge.getWaitingTime(edge_id)
        edge_priority = calc_edge_priority(edge_id, waiting_vehicles, waiting_time)
        if edge_priority > max_priority:
            max_priority = edge_priority
            max_priority_index = i
    return max_priority_index

if __name__ == '__main__':
    fuzzy_logic()