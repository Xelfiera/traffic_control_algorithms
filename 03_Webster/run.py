import traci
from Utils import simulation

def webster():
    simulation.start()
    tl_id = traci.trafficlight.getIDList()[0]

if __name__ == "__main__":
    webster()