import traci
from Utils import simulation
from fuzzy_logic_design import calc_edge_priority

def fuzzy_logic():
    simulation.start()

    while traci.simulation.getTime() < 7200:
        traci.simulationStep()

if __name__ == '__main__':
    fuzzy_logic()