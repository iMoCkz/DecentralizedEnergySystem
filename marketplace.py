class Marketplace:
    def __init__(self, name):
        self.name = name
        self.market_participants = []
        self.electrical_power_price = 1
        self.thermal_power_price = 1

    def register_participant(self, agent):
        if agent not in self.market_participants:
            self.market_participants.append(agent)
            print('{0} has been registered to the marketplace {1}.'.format(agent.name, self.name))

    def request_electrical_energy(self, requesting_agent, requested_amount):
        # get agent which offer electrical power
        candidate_participants = [participant for
                                  participant in self.market_participants if participant.offered_electrical_power > 0]
        # sort them by lowest price
        candidate_participants.sort(key=lambda agent: agent.electrical_power_price, reverse=True)

        print('  {} requests {:.3f}kWh on the market.'.format(requesting_agent.name, requested_amount))
        for agent in candidate_participants:
            if agent.electrical_power_price <= self.electrical_power_price:
                offered_el_power = agent.offered_electrical_power
                # buy as much from an agent as possible
                if agent is not requesting_agent :
                    if offered_el_power - requested_amount >= 0:
                        agent.purchase_electrical_power(requested_amount)
                        print('  {} buys {:.3f}kWh from {}'.format(requesting_agent.name, requested_amount, agent.name))
                        requested_amount = 0
                    else:
                        requested_amount -= offered_el_power
                        agent.purchase_electrical_power(offered_el_power)
                        print('  {} buys {:.3f}kWh from {}'.format(requesting_agent.name, offered_el_power, agent.name))
            # if no more electrical power is needed, leave the market
            if requested_amount == 0:
                break
        # if there is no more agent offering electrical power, requesting agent will buy from the market
        if requested_amount > 0:
            print('  {} buys {:.3f}kWh from grid operator'.format(requesting_agent.name, requested_amount))

    def request_thermal_energy(self, requesting_agent, requested_amount):
        candidate_participants = [participant for
                                  participant in self.market_participants if participant.offered_thermal_power > 0]
        candidate_participants.sort(key=lambda agent: agent.thermal_power_price, reverse=True)

        print('  {} requests {}l on the market.'.format(requesting_agent.name, requested_amount))
        for agent in candidate_participants:
            if agent.thermal_power_price <= self.thermal_power_price:
                offered_tp_power = agent.offered_thermal_power
                # buy as much from an agent as possible
                if agent is not requesting_agent and offered_tp_power > 0:
                    if offered_tp_power - requested_amount >= 0:
                        agent.purchase_thermal_power(requested_amount)
                        print('  {} buys {}l from {}'.format(requesting_agent.name, requested_amount, agent.name))
                        requested_amount = 0
                    else:
                        requested_amount -= offered_tp_power
                        agent.purchase_thermal_power(offered_tp_power)
                        print('  {} buys {}l from {}'.format(requesting_agent.name, offered_tp_power, agent.name))
            # if no more electrical power is needed, leave the market
            if requested_amount == 0:
                break
        # if there is no more agent offering thermal power, requesting agent will buy from the market
        if requested_amount > 0:
            print('  {} buys {}l from grid operator'.format(requesting_agent.name, requested_amount))

