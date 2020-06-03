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





