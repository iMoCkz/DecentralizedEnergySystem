class Marketplace:
    def __init__(self, name):
        self.name = name
        self.market_participants = []

    def register_participant(self, agent):
        if agent not in self.market_participants:
            self.market_participants.append(agent)
            print('{0} has been registered to the marketplace {1}.'.format(agent.name, self.name))

    def request_electrical_energy(self, requesting_agent, requested_amount):
        print('{} requests {}kWh on the market.'.format(requesting_agent.name, requested_amount))
        for agent in self.market_participants:
            offered_el_power = agent.offered_electrical_power
            # buy as much from an agent as possible
            if agent is not requesting_agent and offered_el_power > 0:
                if offered_el_power - requested_amount >= 0:
                    agent.purchase_electrical_power(requested_amount)
                    print('{} buys {}kWh from {}'.format(requesting_agent.name, requested_amount, agent.name))
                else:
                    requested_amount -= offered_el_power
                    agent.offered_electrical_power = 0
                    agent.purchase_electrical_power(offered_el_power)
                    print('{} buys {}kWh from {}'.format(requesting_agent.name, offered_el_power, agent.name))
            # if no more electrical power is needed, leave the market
            if requested_amount == 0:
                break
        # if there is no more agent offering electrical power, requesting agent will buy from the market
        if requested_amount > 0:
            print('{} buys {}kWh from the grid operator'.format(requesting_agent.name, requested_amount))

    def request_thermal_energy(self, requesting_agent, amount):
        pass
