class Marketplace:
    def __init__(self, name):
        self.name = name
        self.market_participants = []

    def register_participant(self, agent):
        if agent not in self.market_participants:
            self.market_participants.append(agent)
            print('{0} has been registered to the marketplace {1}.'.format(agent.name, self.name))

    def request_electrical_energy(self, agent, amount):
        pass

    def request_thermal_energy(self, agent, amount):
        pass
