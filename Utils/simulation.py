import traci
import os

simulation_time = 7200
tl_phases = {"1_0": "rrrrrrrrrrrrrrrrrrGGGGGG",
             "2_0": "rrrrrrGGGGGGrrrrrrrrrrrr",
             "3_0": "rrrrrrrrrrrrGGGGGGrrrrrr",
             "4_0": "GGGGGGrrrrrrrrrrrrrrrrrr"}
tl_yellow_phases = {"1_0": "rrrrrrrrrrrrrrrrrryyyyyy",
                    "2_0": "rrrrrryyyyyyrrrrrrrrrrrr",
                    "3_0": "rrrrrrrrrrrryyyyyyrrrrrr",
                    "4_0": "yyyyyyrrrrrrrrrrrrrrrrrr"}

cur_phase_duration = 0

def start():
    sim_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Intersection")
    sim_file = fr"{sim_path}\kilis.sumocfg"
    traci.start([
        "sumo-gui", "-c", f"{sim_file}", '--start', '--quit-on-end',
        "--statistic-output", r"stats\statistics.stats.xml", "--tripinfo-output", r"stats\tripinfo.trips.xml"
    ])

def get_inc_edges():
    inc_edge_ids = []
    edge_ids = traci.edge.getIDList()
    for edge in edge_ids:
        if edge[2] == '0':
            inc_edge_ids.append(edge)
    return inc_edge_ids

def get_out_edges():
    out_edge_ids = []
    edge_ids = traci.edge.getIDList()
    for edge in edge_ids:
        if edge[2] == '1':
            out_edge_ids.append(edge)
    return out_edge_ids

def set_green_phase(tl_id, edge_id):
    traci.trafficlight.setRedYellowGreenState(tl_id, tl_phases[edge_id])

def set_yellow_phase(tl_id):
    phase_definition = traci.trafficlight.getRedYellowGreenState(tl_id)
    for edge_id in tl_phases.keys():
        if tl_phases[edge_id] == phase_definition:
            traci.trafficlight.setRedYellowGreenState(tl_id, tl_yellow_phases[edge_id])
            break

def set_red_phase(tl_id):
    traci.trafficlight.setRedYellowGreenState(tl_id, "rrrrrrrrrrrrrrrrrrrrrrrr")