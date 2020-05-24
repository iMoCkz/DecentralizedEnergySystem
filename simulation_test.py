from agent import Agent
from marketplace import Marketplace

marketplace = Marketplace('Market1')

a1_data = {'electrical_c': 'Verbrauchsdaten01.csv', 'electrical_p': 'Verbrauchsdaten2.csv'}
agent_1 = Agent('Agent1', a1_data)
agent_1.marketplace = marketplace

agent_2 = Agent('Agent2', a1_data)
agent_2.marketplace = marketplace





