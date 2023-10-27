import traci
from Utils import simulation
from fuzzyST_design import calc_signal_time

def fuzzyst_logic():
    simulation.start()
    signal_arrangement = [0, 3, 1, 2]
    signal_order = 0
    tl_edge_ids = simulation.get_inc_edges()
    tl_id = traci.trafficlight.getIDList()[0]

    while traci.simulation.getTime() < simulation.simulation_time:
        if simulation.cur_phase_duration <= -3:
            print(signal_order)
            signal_edge_id = tl_edge_ids[signal_arrangement[signal_order]]
            no_waiting_vehicles = traci.edge.getLastStepHaltingNumber(signal_edge_id)
            no_lanes_on_edge = traci.edge.getLaneNumber(signal_edge_id)
            simulation.cur_phase_duration = int(calc_signal_time(signal_edge_id,
                                                                 no_waiting_vehicles,
                                                                 no_lanes_on_edge))
            simulation.set_green_phase(tl_id, signal_edge_id)
            signal_order += 1
            if signal_order == 4:
                signal_order = 0
        elif simulation.cur_phase_duration == 0:
            simulation.set_yellow_phase(tl_id)
        simulation.cur_phase_duration -= 1
        traci.simulationStep()

if __name__ == '__main__':
    fuzzyst_logic()