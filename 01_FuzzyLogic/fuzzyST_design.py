import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

no_waiting_vehicles = ctrl.Antecedent(np.arange(0, 13, 1), 'no_waiting_vehicles')
no_lanes_on_edge = ctrl.Antecedent(np.arange(0, 5, 0.5), 'no_lanes_on_edge')

signal_time = ctrl.Consequent(np.arange(0, 51, 1), 'signal_time')

no_waiting_vehicles['less'] = fuzzy.zmf(no_waiting_vehicles.universe, 2, 4)
no_waiting_vehicles['medium'] = fuzzy.trimf(no_waiting_vehicles.universe, [3, 5, 7])
no_waiting_vehicles['high'] = fuzzy.trimf(no_waiting_vehicles.universe, [6, 8, 9])
no_waiting_vehicles['too-high'] = fuzzy.smf(no_waiting_vehicles.universe, 8, 10)
# no_waiting_vehicles.view()

no_lanes_on_edge['one'] = fuzzy.trimf(no_lanes_on_edge.universe, [0.5, 1, 1.5])
no_lanes_on_edge['two'] = fuzzy.trimf(no_lanes_on_edge.universe, [1.5, 2, 2.5])
no_lanes_on_edge['three'] = fuzzy.trimf(no_lanes_on_edge.universe, [2.5, 3, 3.5])
no_lanes_on_edge['four'] = fuzzy.smf(no_lanes_on_edge.universe, 3.5, 4)
# no_lanes_on_edge.view()

signal_time['short'] = fuzzy.zmf(signal_time.universe, 5, 10)
signal_time['medium'] = fuzzy.trimf(signal_time.universe, [7, 15, 25])
signal_time['long'] = fuzzy.trimf(signal_time.universe, [20, 27, 35])
signal_time['too-long'] = fuzzy.smf(signal_time.universe, 30, 40)
# signal_time.view()

rule_a0 = ctrl.Rule(no_waiting_vehicles['less'] & no_lanes_on_edge['one'], signal_time['medium'])
rule_b0 = ctrl.Rule(no_waiting_vehicles['medium'] & no_lanes_on_edge['one'], signal_time['long'])
rule_c0 = ctrl.Rule(no_waiting_vehicles['high'] & no_lanes_on_edge['one'], signal_time['long'])
rule_d0 = ctrl.Rule(no_waiting_vehicles['too-high'] & no_lanes_on_edge['one'], signal_time['too-long'])

rule_a1 = ctrl.Rule(no_waiting_vehicles['less'] & no_lanes_on_edge['two'], signal_time['medium'])
rule_b1 = ctrl.Rule(no_waiting_vehicles['medium'] & no_lanes_on_edge['two'], signal_time['medium'])
rule_c1 = ctrl.Rule(no_waiting_vehicles['high'] & no_lanes_on_edge['two'], signal_time['long'])
rule_d1 = ctrl.Rule(no_waiting_vehicles['too-high'] & no_lanes_on_edge['two'], signal_time['long'])

rule_a2 = ctrl.Rule(no_waiting_vehicles['less'] & no_lanes_on_edge['three'], signal_time['short'])
rule_b2 = ctrl.Rule(no_waiting_vehicles['medium'] & no_lanes_on_edge['three'], signal_time['medium'])
rule_c2 = ctrl.Rule(no_waiting_vehicles['high'] & no_lanes_on_edge['three'], signal_time['medium'])
rule_d2 = ctrl.Rule(no_waiting_vehicles['too-high'] & no_lanes_on_edge['three'], signal_time['long'])

rule_a3 = ctrl.Rule(no_waiting_vehicles['less'] & no_lanes_on_edge['four'], signal_time['short'])
rule_b3 = ctrl.Rule(no_waiting_vehicles['medium'] & no_lanes_on_edge['four'], signal_time['short'])
rule_c3 = ctrl.Rule(no_waiting_vehicles['high'] & no_lanes_on_edge['four'], signal_time['medium'])
rule_d3 = ctrl.Rule(no_waiting_vehicles['too-high'] & no_lanes_on_edge['four'], signal_time['medium'])

signal_time_ctrl = ctrl.ControlSystem([rule_a0, rule_b0, rule_c0, rule_d0,
                                       rule_a1, rule_b1, rule_c1, rule_d1,
                                       rule_a2, rule_b2, rule_c2, rule_d2,
                                       rule_a3, rule_b3, rule_c3, rule_d3,])
signal_time_status = ctrl.ControlSystemSimulation(signal_time_ctrl)

def calc_signal_time(edge_id, waiting_vehicles, lanes_on_edge):
    if waiting_vehicles == 0:
        return 0
    signal_time_status.input['no_waiting_vehicles'] = waiting_vehicles
    signal_time_status.input['no_lanes_on_edge'] = lanes_on_edge
    signal_time_status.compute()
    signal_time_output = signal_time_status.output['signal_time']

    print(f"Number of waiting vehicles on {edge_id}: {waiting_vehicles}")
    print(f"Number of lanes on {edge_id}: {lanes_on_edge}")
    print(f"Signal time of {edge_id}: {signal_time_output}")

    return signal_time_output