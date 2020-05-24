import csv


def _read_file(path):
    with open(path) as fp:
        reader = csv.reader(fp, delimiter=";")
        next(reader, None)  # skip the headers
        return [row for row in reader]


class Agent:
    def __init__(self, name, data):
        self.name = name
        self._market = None

        self._electrical_reserve_fund = 0
        self._thermal_reserve_fund = 0

        self.electrical_consumption = 0
        # self.electrical_production = 0
        self.electrical_storage = 0
        self.thermal_consumption = 0
        # self.thermal_production = 0
        self.thermal_storage = 0

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

    @property
    def marketplace(self):
        return self._market

    @marketplace.setter
    def marketplace(self, market):
        self._market = market
        self._market.register_participant(self)

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

    def step(self):
        # energy turnover
        if self._electrical_production_data is not None:
            self._electrical_storage += self._electrical_production_data.pop(0)

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







