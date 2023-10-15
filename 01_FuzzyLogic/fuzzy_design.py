import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

no_waiting_vehicles = ctrl.Antecedent(np.arange(0, 13, 1), 'no_waiting_vehicles')
avg_waiting_time = ctrl.Antecedent(np.arange(0, 51, 1), 'avg_waiting_time')

edge_priority = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'priority')

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

edge_priority['low'] = fuzzy.trimf(edge_priority.universe, [0, 0, 0.2])
edge_priority['medium'] = fuzzy.trimf(edge_priority.universe, [0.1, 0.4, 0.6])
edge_priority['high'] = fuzzy.trimf(edge_priority.universe, [0.5, 0.7, 0.8])
edge_priority['too-high'] = fuzzy.smf(edge_priority.universe, 0.75, 0.9)
# edge_priority.view()

rule_a0 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['short'], edge_priority['low'])
rule_b0 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['short'], edge_priority['low'])
rule_c0 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['short'], edge_priority['medium'])
rule_d0 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['short'], edge_priority['medium'])

rule_a1 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['medium'], edge_priority['low'])
rule_b1 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['medium'], edge_priority['medium'])
rule_c1 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['medium'], edge_priority['medium'])
rule_d1 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['medium'], edge_priority['high'])

rule_a2 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['long'], edge_priority['medium'])
rule_b2 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['long'], edge_priority['medium'])
rule_c2 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['long'], edge_priority['high'])
rule_d2 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['long'], edge_priority['high'])

rule_a3 = ctrl.Rule(no_waiting_vehicles['less'] & avg_waiting_time['too-long'], edge_priority['high'])
rule_b3 = ctrl.Rule(no_waiting_vehicles['medium'] & avg_waiting_time['too-long'], edge_priority['high'])
rule_c3 = ctrl.Rule(no_waiting_vehicles['high'] & avg_waiting_time['too-long'], edge_priority['too-high'])
rule_d3 = ctrl.Rule(no_waiting_vehicles['too-high'] & avg_waiting_time['too-long'], edge_priority['too-high'])

edge_priority_ctrl = ctrl.ControlSystem([rule_a0, rule_b0, rule_c0, rule_d0,
                                         rule_a1, rule_b1, rule_c1, rule_d1,
                                         rule_a2, rule_b2, rule_c2, rule_d2,
                                         rule_a3, rule_b3, rule_c3, rule_d3,])
edge_priority_status = ctrl.ControlSystemSimulation(edge_priority_ctrl)

def calc_edge_priority(edge_id, waiting_vehicles, waiting_time):
    edge_priority_status.input['no_waiting_vehicles'] = waiting_vehicles
    if waiting_vehicles != 0:
        edge_priority_status.input['avg_waiting_time'] = waiting_time / waiting_vehicles
    else:
        edge_priority_status.input['avg_waiting_time'] = 0
    edge_priority_status.compute()
    priority_output = edge_priority_status.output['priority']

    print('\n')
    print(f"Number of waiting vehicles in {edge_id}: {waiting_vehicles}")
    if waiting_vehicles != 0:
        print(f"Average waiting time of vehicles in {edge_id}: {waiting_time / waiting_vehicles}")
    else:
        print(f"Average waiting time of vehicles in {edge_id}: 0")
    print(f"Priority of {edge_id}: {priority_output}")

    return priority_output