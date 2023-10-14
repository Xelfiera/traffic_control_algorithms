import traci
from Utils import simulation

def fuzzy_logic():
    simulation.start()

    while traci.simulation.getTime() < 7200:
        traci.simulationStep()

        # processing...

if __name__ == '__main__':
    fuzzy_logic()