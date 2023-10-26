import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

no_waiting_vehicles = ctrl.Antecedent(np.arange(0, 13, 1), 'no_waiting_vehicles')
no_lanes_on_edge = ctrl.Antecedent(np.arange(0, 5, 0.5), 'no_lanes_on_edges')

signal_time = ctrl.Consequent(np.arange(0, ))

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