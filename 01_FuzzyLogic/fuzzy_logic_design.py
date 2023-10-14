import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

no_waiting_vehicles = ctrl.Antecedent(np.arange(0, 13, 1), 'no_waiting_vehicles')
avg_waiting_time = ctrl.Antecedent(np.arange(0, 51, 1), 'avg_waiting_time')

lane_priority = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'priority')

no_waiting_vehicles['less'] = fuzzy.zmf(no_waiting_vehicles.universe, 2, 4)
no_waiting_vehicles['medium'] = fuzzy.trimf(no_waiting_vehicles.universe, [3, 5, 7])
no_waiting_vehicles['high'] = fuzzy.trimf(no_waiting_vehicles.universe, [6, 8, 9])
no_waiting_vehicles['too-high'] = fuzzy.smf(no_waiting_vehicles.universe, 8, 10)
# no_waiting_vehicles.view()

avg_waiting_time['short'] = fuzzy.zmf(avg_waiting_time.universe, 5, 10)
avg_waiting_time['medium'] = fuzzy.trimf(avg_waiting_time.universe, [5, 15, 20])
avg_waiting_time['long'] = fuzzy.trimf(avg_waiting_time.universe, [17, 25, 35])
avg_waiting_time['too-long'] = fuzzy.smf(avg_waiting_time.universe, 30, 40)
# avg_waiting_time.view()

lane_priority['low'] = fuzzy.trimf(lane_priority.universe, [0, 0, 0.2])
lane_priority['medium'] = fuzzy.trimf(lane_priority.universe, [0.1, 0.4, 0.6])
lane_priority['high'] = fuzzy.trimf(lane_priority.universe, [0.5, 0.7, 0.8])
lane_priority['too-high'] = fuzzy.smf(lane_priority.universe, 0.75, 0.9)
# lane_priority.view()

rule_a0 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['short'], lane_priority['low'])
rule_b0 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['short'], lane_priority['low'])
rule_c0 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['short'], lane_priority['medium'])
rule_d0 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['short'], lane_priority['medium'])

rule_a1 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['medium'], lane_priority['low'])
rule_b1 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['medium'], lane_priority['medium'])
rule_c1 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['medium'], lane_priority['medium'])
rule_d1 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['medium'], lane_priority['high'])

rule_a2 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['long'], lane_priority['medium'])
rule_b2 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['long'], lane_priority['medium'])
rule_c2 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['long'], lane_priority['high'])
rule_d2 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['long'], lane_priority['high'])

rule_a3 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['too-long'], lane_priority['high'])
rule_b3 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['too-long'], lane_priority['high'])
rule_c3 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['too-long'], lane_priority['too-high'])
rule_d3 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['too-long'], lane_priority['too-high'])

lane_priority_ctrl = ctrl.ControlSystem([rule_a0, rule_b0, rule_c0, rule_d0,
                                         rule_a1, rule_b1, rule_c1, rule_d1,
                                         rule_a2, rule_b2, rule_c2, rule_d2,
                                         rule_a3, rule_b3, rule_c3, rule_d3,])
lane_priority_status = ctrl.ControlSystemSimulation(lane_priority_ctrl)

def calc_edge_priority(lane_id, waiting_vehicles, waiting_time):
    lane_priority_status.input['no_waiting_vehicles'] = waiting_vehicles
    lane_priority_status.input['avg_waiting_time'] = waiting_time / waiting_vehicles
    lane_priority_status.compute()
    priority_output = lane_priority_status.output['lane_priority']

    print(f"Number of waiting vehicles in {lane_id}: {waiting_vehicles}")
    print(f"Average waiting time of vehicles in {lane_id}: {waiting_time / waiting_vehicles}")
    print(f"Priority of {lane_id}: {priority_output}")

    return priority_output