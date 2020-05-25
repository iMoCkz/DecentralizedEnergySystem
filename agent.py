import csv


def _read_file(path):
    with open(path) as fp:
        reader = csv.reader(fp, delimiter=";")
        next(reader, None)  # skip the headers
        return [row for row in reader]


class Agent:
    def __init__(self, name, data):
        self.name = name
        self._withdraw_factor = 0.8
        self._market = None

        self.electrical_consumption = 0
        self.electrical_storage = 0
        self.thermal_consumption = 0
        self.thermal_storage = 0

        self._offered_electrical_power = 0
        self._offered_thermal_power = 0

        self._electrical_consumption_data = None
        self._electrical_production_data = None
        self._electrical_storage_data = None
        self._thermal_consumption_data = None
        self._thermal_production_data = None
        self._thermal_storage_data = None

        # Dateien einlesen
        for key, val in data.items():
            self._get_data(key, val)

        # test = self._electrical_consumption_data[:5]

    def _get_data(self, key, path):
        if key == 'electrical_c':
            self._electrical_consumption_data = _read_file(path)
        elif key == 'thermal_c':
            self._thermal_consumption_data = _read_file(path)
        elif key == 'electrical_p':
            self._electrical_production_data = _read_file(path)
        elif key == 'thermal_p':
            self._thermal_production_data = _read_file(path)
        elif key == 'electrical_s':
            self._electrical_storage_data = _read_file(path)
        elif key == 'thermal_s':
            self._thermal_storage_data = _read_file(path)

    @property
    def marketplace(self):
        return self._market

    @marketplace.setter
    def marketplace(self, market):
        self._market = market
        self._market.register_participant(self)

    @property
    def offered_electrical_power(self):
        return self._offered_electrical_power

    def purchase_electrical_power(self, withdrawal):
        if self._offered_electrical_power - withdrawal >= 0:
            self._offered_electrical_power -= withdrawal
            self.electrical_storage -= withdrawal
        else:
            print('Error while withdrawing electrical power.')

    @property
    def offered_thermal_power(self):
        return self._offered_thermal_power

    def purchase_thermal_power(self, withdrawal):
        if self._offered_thermal_power - withdrawal >= 0:
            self._offered_thermal_power -= withdrawal
            self.thermal_storage -= withdrawal
        else:
            print('Error while withdrawing thermal power.')

    def step(self):
        # energy turnover
        if self._electrical_production_data is not None:
            self._electrical_storage += self._electrical_production_data.pop(0)
            self._offered_electrical_power *= self._withdraw_factor

        if self._electrical_consumption_data is not None:
            consumption = self._electrical_consumption_data.pop(0)
            if self.electrical_storage >= consumption:
                self.electrical_storage -= consumption
            else:
                # deplete current electrical storage
                consumption -= self.electrical_storage
                self.electrical_storage = 0
                # request on market
                self._market.request_electrical_energy(self, consumption)

        # thermal turnover
        if self._thermal_production_data is not None:
            self._thermal_storage += self._thermal_production_data.pop(0)
            self._offered_thermal_power *= self._withdraw_factor

        if self._thermal_consumption_data is not None:
            consumption = self._thermal_consumption_data.pop(0)
            if self.thermal_storage >= consumption:
                self.thermal_storage -= consumption
            else:
                # deplete current thermal storage
                consumption -= self.thermal_storage
                self.thermal_storage = 0
                # request on market
                self._market.request_thermal_energy(self, consumption)






