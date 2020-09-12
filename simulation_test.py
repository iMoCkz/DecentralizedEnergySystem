# diese Datei wird ausgeführt

# importiere unsere beiden anderen Klassen Agent und Marketplace, sowie ein Modul zum nutzen von Zeitfunktionen
import time
from agent import Agent
from marketplace import Marketplace

# erstelle den Markt
marketplace = Marketplace('Market1')

# Dictionary, welches die Daten des Agenten mit dem ensprechenden Namen (siehe "_get_data" in Agent-Klasse)
a1_data = {'electrical_c': 'SumProfiles.Electricity_1.csv',
           'thermal_c': 'SumProfiles.WarmWater_1.csv',
           'electrical_p': 'PVAnlage_1.csv'}
# erstelle Agenten mit zugehörigen Daten
agent_1 = Agent('Agent1', a1_data)
# setze den Markt des Agenten auf den vorher erstellten Markt
agent_1.marketplace = marketplace

# zweiter Agent mit denselben Schritten wie bei Agent 1
a1_data = {'electrical_c': 'SumProfiles.Electricity_2.csv',
           'thermal_c': 'SumProfiles.WarmWater_2.csv'}
agent_2 = Agent('Agent2', a1_data)
agent_2.marketplace = marketplace
print()

# durchlaufe geladene Daten der Agenten solange jeder Agent noch Daten im Stack hat
while agent_1.has_next() and agent_2.has_next():
    # Entnimm Zeitangaben aus Agenten 1 (Agent 2 wäre genauso möglich)
    print(agent_1.dates.pop(0))
    # load data
    print('Electricity:')
    agent_1.load_electricity_step_data()
    agent_2.load_electricity_step_data()
    # if possible, do self consumption
    agent_1.electrical_self_consumption()
    agent_2.electrical_self_consumption()
    # if needed, buy on market
    agent_1.purchase_electricity_on_market()
    agent_2.purchase_electricity_on_market()
    print('Thermal energy:')
    agent_1.load_thermal_step_data()
    agent_2.load_thermal_step_data()
    # if possible, do self consumption
    agent_1.thermal_self_consumption()
    agent_2.thermal_self_consumption()
    # if needed, buy on market
    agent_1.purchase_thermal_energy_on_market()
    agent_2.purchase_thermal_energy_on_market()
    # warte 1s, um Text in Konsole lesbar zu halten
    time.sleep(1)
    print('__________________________________________')

print('Finished.')





