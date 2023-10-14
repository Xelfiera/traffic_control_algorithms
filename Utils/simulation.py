import traci
import os

tl_phases = {"1_0": "rrrrrrrrrrrrrrrrrrGGGGGG",
             "2_0": "rrrrrrGGGGGGrrrrrrrrrrrr",
             "3_0": "rrrrrrrrrrrrGGGGGGrrrrrr",
             "4_0": "GGGGGGrrrrrrrrrrrrrrrrrr"}

def start():
    sim_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Intersection")
    sim_file = fr"{sim_path}\kilis.sumocfg"
    traci.start([
        "sumo-gui", "-c", f"{sim_file}", '--start', '--quit-on-end',
        "--statistic-output", "stats\\statistics.stats.xml", "--tripinfo-output", "stats\\tripinfo.trips.xml"
    ])

def get_inc_edges():
    inc_edge_ids = []
    edge_ids = traci.edge.getIDList()
    for edge in edge_ids:
        if edge[2] == '0':
            inc_edge_ids.append(edge)
    return inc_edge_ids

def set_phase(tl_id, edge_id):
    traci.trafficlight.setCompleteRedYellowGreenDefinition(tl_id, tl_phases[edge_id])