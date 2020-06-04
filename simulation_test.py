import time
from agent import Agent
from marketplace import Marketplace

marketplace = Marketplace('Market1')

a1_data = {'electrical_c': 'SumProfiles.Electricity_1.csv',
           'thermal_c': 'SumProfiles.WarmWater_1.csv',
           'electrical_p': 'PVAnlage_1.csv'}
agent_1 = Agent('Agent1', a1_data)
agent_1.marketplace = marketplace

a1_data = {'electrical_c': 'SumProfiles.Electricity_2.csv',
           'thermal_c': 'SumProfiles.WarmWater_2.csv'}
agent_2 = Agent('Agent2', a1_data)
agent_2.marketplace = marketplace
print()

while agent_1.has_next() and agent_2.has_next():
    # load data
    agent_1.load_step_data()
    agent_2.load_step_data()
    # if possible, do self consumption
    agent_1.self_consumption()
    agent_2.self_consumption()
    # if needed, buy on market
    agent_1.purchase_on_market()
    agent_2.purchase_on_market()
    #
    time.sleep(2)
    print()

print("Finished.")





