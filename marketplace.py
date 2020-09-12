# Markt-Klasse, die den Markt repräsentiert
class Marketplace:
    # Konstruktor, der einen Namen als Übergabeparameter erwartet
    def __init__(self, name):
        self.name = name
        # Liste der Marktteilnehmer (Anzahl der Teilnehmer nicht begrenzt)
        self.market_participants = []

    # registriert/fügt Teilnehmer dem Markt hinzu, wenn Teilnehmer bisher nicht am Markt
    def register_participant(self, agent):
        if agent not in self.market_participants:
            self.market_participants.append(agent)
            print('{0} has been registered to the marketplace {1}.'.format(agent.name, self.name))

    # Funktion, die einen bestimmten Agenten eine bestimmte Menge an elektrischen Strom am Markt anfragen lässt
    def request_electrical_energy(self, requesting_agent, requested_amount):
        print('  {} requests {:.3f}kWh on the market.'.format(requesting_agent.name, requested_amount))
        # durchlaufe jeden möglichen Marktteilnehmer
        for agent in self.market_participants:
            # finde heraus, woe viel ein bestimmter Teilnehmer am Markt anbietet
            offered_el_power = agent.offered_electrical_power
            # wenn der Teilnehmer nicht er selbst ist und er elektrische Energie anbietet, wollen wir kaufen
            if agent is not requesting_agent and offered_el_power > 0:
                # wenn das Angebot des anbietenden Agenten größer als das die Nachfrage ist, kauf alles bei ihm
                if offered_el_power - requested_amount >= 0:
                    agent.purchase_electrical_power(requested_amount)
                    print('  {} buys {:.3f}kWh from {}'.format(requesting_agent.name, requested_amount, agent.name))
                    requested_amount = 0
                else:
                    # falls das Angebot nicht komplett die Nachfrage deckt, kaufe zumindest so viel wie möglich
                    requested_amount -= offered_el_power
                    agent.purchase_electrical_power(offered_el_power)
                    print('  {} buys {:.3f}kWh from {}'.format(requesting_agent.name, offered_el_power, agent.name))
            # if no more electrical power is needed, leave the market (otherwise request next agent)
            if requested_amount == 0:
                break
        # if there is no more agent offering electrical power, requesting agent will buy from the market
        if requested_amount > 0:
            print('  {} buys {:.3f}kWh from grid operator'.format(requesting_agent.name, requested_amount))

    # siehe "request_electrical_energy" nur mit thermischer Energie
    def request_thermal_energy(self, requesting_agent, requested_amount):
        print('  {} requests {}l on the market.'.format(requesting_agent.name, requested_amount))
        for agent in self.market_participants:
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
            # if no more electrical power is needed, leave the market (otherwise request next agent)
            if requested_amount == 0:
                break
        # if there is no more agent offering thermal power, requesting agent will buy from the market
        if requested_amount > 0:
            print('  {} buys {}l from grid operator'.format(requesting_agent.name, requested_amount))
