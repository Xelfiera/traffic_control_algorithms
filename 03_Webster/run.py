import traci
import time
from Utils import simulation

index = 0
timer = 0

def webster():
    global index
    global timer
    simulation.start()
    edge_ids = simulation.get_inc_edges()
    tl_id = traci.trafficlight.getIDList()[0]
    green_times = [9, 4, 8, 2]
    indexes = [0, 3, 1, 2]
    while traci.simulation.getTime() < simulation.simulation_time:
        set_phase(green_times[indexes[index]], tl_id, edge_ids[indexes[index]])
        traci.simulationStep()

def set_phase(green_time, tl_id, edge_id):
    global timer
    global index
    if timer < green_time:
        simulation.set_green_phase(tl_id, edge_id)
    elif green_time <= timer < green_time + 2:
        simulation.set_yellow_phase(tl_id)
    elif timer == green_time + 2:
        timer = 0
        index += 1
        if index == 4:
            index = 0
    timer += 1

if __name__ == "__main__":
    webster()