import csv


def _read_file(path, delimiter):
    with open(path) as fp:
        reader = csv.reader(fp, delimiter=delimiter)
        next(reader, None)  # skip the headers
        return [row for row in reader if row]


def _pool_values(matrix, pool_cnt):
    index = 0
    squeezed_m = []

    for idx in range(0, len(matrix), pool_cnt):
        squeezed_m.append([index,
                           matrix[idx][1],
                           round(sum([float(row[2]) for row in matrix[idx:idx + pool_cnt]]), 3)])
        index = index + 1

    return squeezed_m


def _cut_to_essential(matrix, columns):
    # remove first 3 rows
    matrix = matrix[3:]
    # only extract needed columns
    matrix = [column[idx] for column in matrix for idx in columns]
    # compresses columns to multiple rows
    matrix = zip(*[iter(matrix)] * len(columns))
    matrix = [list(row) for row in matrix]

    return matrix


class Agent:
    def __init__(self, name, data):
        self.name = name
        self._market = None
        self.dates = []

        self._total_electrical_consumption = 0
        self._electricity_to_request = 0
        self._electrical_storage = 0

        self._total_thermal_consumption = 0
        self._thermal_energy_to_request = 0
        self._thermal_storage = 0

        self._offered_electrical_power = 0
        self._offered_thermal_power = 0

        self._electrical_power_price = 0
        self._thermal_power_price = 0

        self._electrical_consumption_data = None
        self._electrical_production_data = None
        self._thermal_consumption_data = None
        self._thermal_production_data = None

        # Dateien einlesen
        for key, val in data.items():
            self._get_data(key, val)

    def _get_data(self, key, path):
        if key == 'electrical_c':
            self._electrical_consumption_data = _read_file(path, ';')
            self._electrical_consumption_data = _pool_values(self._electrical_consumption_data, 60)
            # remove leap day (29.02.2016
            del self._electrical_consumption_data[1416:1440]
            # dates
            self.dates = [row[1] for row in self._electrical_consumption_data]
        elif key == 'thermal_c':
            self._thermal_consumption_data = _read_file(path, ';')
            self._thermal_consumption_data = _pool_values(self._thermal_consumption_data, 60)
            # remove leap day
            del self._thermal_consumption_data[1416:1440]
        elif key == 'electrical_p':
            self._electrical_production_data = _read_file(path, ',')
            self._electrical_production_data = _cut_to_essential(self._electrical_production_data, [0, 2])
        elif key == 'thermal_p':
            self._thermal_production_data = _read_file(path, ',')
            self._thermal_production_data = _cut_to_essential(self._thermal_production_data, [0, 2])

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
            self._electrical_storage -= withdrawal
        else:
            print('Error while withdrawing electrical power.')

    @property
    def offered_thermal_power(self):
        return self._offered_thermal_power

    @property
    def electrical_power_price(self):
        return self._electrical_power_price

    @electrical_power_price.setter
    def electrical_power_price(self, price):
        self._electrical_power_price = price

    @property
    def thermal_power_price(self):
        return self._thermal_power_price

    @thermal_power_price.setter
    def thermal_power_price(self, price):
        self._thermal_power_price = price

    def purchase_thermal_power(self, withdrawal):
        if self._offered_thermal_power - withdrawal >= 0:
            self._offered_thermal_power -= withdrawal
            self.thermal_storage -= withdrawal
        else:
            # should not happen based on marketplace logic
            print('Error while withdrawing thermal power.')

    def has_next(self):
        return len(self._electrical_consumption_data) > 0 and len(self._thermal_consumption_data) > 0

    def load_electricity_step_data(self):
        if self._electrical_production_data is not None:
            self._electrical_storage += float(self._electrical_production_data.pop(0)[1])
            print("  {} electrical storage: {:.3f}kWh".format(self.name, self._electrical_storage))

        if self._electrical_consumption_data is not None:
            self._total_electrical_consumption = self._electrical_consumption_data.pop(0)[2]
            print("  {} electrical consumption: {:.3f}kWh".format(self.name, self._total_electrical_consumption))

    def electrical_self_consumption(self):
        if self._electrical_storage > 0 and self._electrical_storage >= self._total_electrical_consumption:
            self._electrical_storage -= self._total_electrical_consumption
        else:
            # deplete current electrical storage
            self._electricity_to_request = self._total_electrical_consumption - self._electrical_storage
            self._electrical_storage = 0
        # set amount to offer on marketplace
        self._offered_electrical_power = self._electrical_storage

    def purchase_electricity_on_market(self):
        if self._electricity_to_request > 0:
            self._market.request_electrical_energy(self, self._electricity_to_request)

    def load_thermal_step_data(self):
        if self._thermal_production_data is not None:
            self._thermal_storage += float(self._thermal_production_data.pop(0)[1])
            print("  {} thermal storage: {}l".format(self.name, self._thermal_storage))

        if self._thermal_consumption_data is not None:
            self._total_thermal_consumption = self._thermal_consumption_data.pop(0)[2]
            print("  {} thermal consumption: {}l".format(self.name, self._total_thermal_consumption))

    def thermal_self_consumption(self):
        if self._thermal_storage > 0 and self._thermal_storage >= self._total_thermal_consumption:
            self._thermal_storage -= self._total_thermal_consumption
        else:
            # deplete current electrical storage
            self._thermal_energy_to_request = self._total_thermal_consumption - self._thermal_storage
            self._thermal_storage = 0
        # set amount to offer on marketplace
        self._offered_thermal_power = self._thermal_storage

    def purchase_thermal_energy_on_market(self):
        if self._thermal_energy_to_request > 0:
            self._market.request_thermal_energy(self, self._thermal_energy_to_request)



