import traci
import os

def start():
    sim_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Intersection")
    sim_file = fr"{sim_path}\kilis.sumocfg"
    traci.start([
        "sumo-gui", "-c", f"{sim_file}", '--start', '--quit-on-end',
        "--statistic-output", "stats\\statistics.stats.xml", "--tripinfo-output", "stats\\tripinfo.trips.xml"
    ])

if __name__ == "__main__":
    start()