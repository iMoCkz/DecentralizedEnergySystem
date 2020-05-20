import csv


def _read_file(path):
    with open(path) as fp:
        reader = csv.reader(fp, delimiter=";")
        next(reader, None)  # skip the headers
        return [row for row in reader]


class Agent:
    def __init__(self, data):
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

        test = self._electrical_consumption_data[:5]

        print(test.pop(0))
        print(test.pop(0))
        print(test.pop(0))
        print(test.pop(0))
        print(test.pop(0))


    def _get_data(self, key, value):
        if key == 'electrical_c':
            self._electrical_consumption_data = _read_file(value)
        elif key == 'thermal_c':
            self._thermal_consumption_data = _read_file(value)
        elif key == 'electrical_p':
            self._electrical_production_data = _read_file(value)
        elif key == 'thermal_p':
            self._thermal_production_data = _read_file(value)
        elif key == 'electrical_s':
            self._electrical_storage_data = _read_file(value)
        elif key == 'thermal_s':
            self._thermal_storage_data = _read_file(value)

    def step(self):
        if self._electrical_production_data is not None:
            self._electrical_storage += self._electrical_production_data.pop(0)
        if self._electrical_consumption_data is not None:
            consumption = self._electrical_consumption_data.pop(0)

            if self.electrical_storage >= consumption:
                self.electrical_storage -= consumption
            else:
                if self.electrical_storage - consumption





