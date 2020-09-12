import csv


# liest File mit gegebenen Trennzeichen (meistens und hier ";") ein
def _read_file(path, delimiter):
    with open(path) as fp:
        reader = csv.reader(fp, delimiter=delimiter)
        # überspringt Header
        next(reader, None)
        # gibt alle nicht-leeren Zeilen zurück
        return [row for row in reader if row]


# fasst relevante Daten zusammen und setzt neue indizes
def _pool_values(matrix, pool_cnt):
    index = 0
    squeezed_m = []
    # durchläuft Daten in gegebener Spanne und fasst x Werte (hier alle Werte einer Stunde) zusammen und rundet auf
    # 3 Nachkommastellen genau
    for idx in range(0, len(matrix), pool_cnt):
        # Array beinhaltet nun [Index, Datum, Summe des Tagesverbrauchs]
        squeezed_m.append([index,
                           matrix[idx][1],
                           round(sum([float(row[2]) for row in matrix[idx:idx + pool_cnt]]), 3)])
        index = index + 1

    return squeezed_m


# entnimm der Matrix nur relevante Spalten und gib für jede Zeile eine Liste zurück
# Rückgabewerte: Liste von Listen
# bezogen auf PVAnlage_1.csv:
# Relevant: time,local_time,electricity
# Irrelevant: irradiance_direct,irradiance_diffuse,temperature
def _cut_to_essential(matrix, columns):
    # remove first 3 rows
    matrix = matrix[3:]
    # only extract needed columns
    matrix = [column[idx] for column in matrix for idx in columns]
    # compresses columns to multiple rows
    matrix = zip(*[iter(matrix)] * len(columns))
    matrix = [list(row) for row in matrix]

    return matrix


# Agenten-Klasse, die einen Akteur auf dem Markt darstellt
class Agent:
    # Konstruktor, der den Namen und entsprechende Daten als Übergabeparameter erwartet
    def __init__(self, name, data):
        # Name wird gespeichert, um Agenten zu unterscheiden
        # restliche Variablen werden im Verlauf benötigt
        self.name = name
        # Akteur wird einem Markt zugeordnet; zu Beginn keine Zuordnung
        self._market = None
        # Zeitpunkte, die durch die csv-Dateinen gegeben sind
        self.dates = []
        # Verbrauch, Nachfrage und Speicher von elektrischer Engergie
        self._total_electrical_consumption = 0
        self._electricity_to_request = 0
        self._electrical_storage = 0
        # Verbrauch, Nachfrage und Speicher von thermischer Engergie
        self._total_thermal_consumption = 0
        self._thermal_energy_to_request = 0
        self._thermal_storage = 0
        # elektrische und thermische Energie, die durch Überschuss am Markt angeboten werden kann
        self._offered_electrical_power = 0
        self._offered_thermal_power = 0
        # Übergebene Daten aus csv-Dateien,
        # die bestimmen, welche Arten von Energie vom Akteur verbraucht und verkauft werden können
        self._electrical_consumption_data = None
        self._electrical_production_data = None
        self._thermal_consumption_data = None
        self._thermal_production_data = None

        # Dateien einlesen
        for key, val in data.items():
            self._get_data(key, val)

    # Daten einlesen und weiter vorverarbeiten je nach Art der Daten
    def _get_data(self, key, path):
        # c: consumption | p: production
        if key == 'electrical_c':
            # lese Dateien mit Trennzeichen ";" ein
            self._electrical_consumption_data = _read_file(path, ';')
            # fasse 60 Daten einer Stunde zu einem Datenpunkt (1 Datenpunkt pro Stunde) zusammen
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
            # entnehme den Daten nur die relevanten Spalten; hier Spalten 0, 1, 2
            self._electrical_production_data = _cut_to_essential(self._electrical_production_data, [0, 2])
        elif key == 'thermal_p':
            self._thermal_production_data = _read_file(path, ',')
            self._thermal_production_data = _cut_to_essential(self._thermal_production_data, [0, 2])

    # getter, um den aktullen Marktplatz des Agenten zu bekommen
    @property
    def marketplace(self):
        return self._market

    # setter, um aktuellen Marktplatz des Agenten zu setzen und den Agenten beim Marktplatz zu registrieren
    @marketplace.setter
    def marketplace(self, market):
        self._market = market
        self._market.register_participant(self)

    # getter, um elektrische Energie zu bekommen, die der Agent am Markt anbietet
    @property
    def offered_electrical_power(self):
        return self._offered_electrical_power

    # Funktion, um elektrische Energie vom Agenten zu kaufen
    def purchase_electrical_power(self, withdrawal):
        # Kauf wird nur getätigt, wenn nicht mehr Energie bezogen, als angeboten wird
        if self._offered_electrical_power - withdrawal >= 0:
            # subtrahiere die bezogene Menge vom Angebot
            self._offered_electrical_power -= withdrawal
            # subtrahiere die bezogene Menge vom eigenen Speicher
            self._electrical_storage -= withdrawal
        else:
            print('Error while withdrawing electrical power.')

    # getter, um thermische Energie zu bekommen, die der Agent am Markt anbietet
    @property
    def offered_thermal_power(self):
        return self._offered_thermal_power

    # gleiches Vorgehen wie bei "purchase_electrical_power" nur mit thermischer Energie
    def purchase_thermal_power(self, withdrawal):
        if self._offered_thermal_power - withdrawal >= 0:
            self._offered_thermal_power -= withdrawal
            self.thermal_storage -= withdrawal
        else:
            # should not happen based on marketplace logic
            print('Error while withdrawing thermal power.')

    # gibt zurück, ob noch Datenpunkte für elektrische und thermische Energie vorliegen
    # da als Datenstruktur ein Stack verwendet wird (um Daten sukzessiv zu verringern),
    # wird die Anzahl der Daten bei jedem Schritt verringert und erreicht am Ende 0,
    # was einer kompletten Abarbeitung der Daten entspricht
    def has_next(self):
        return len(self._electrical_consumption_data) > 0 and len(self._thermal_consumption_data) > 0

    # lade nächsten Datenpunkt/Zeitschritt aus Stack
    def load_electricity_step_data(self):
        # Elektrische Produktion laden funktioniert nur, wenn noch Daten im Stack vorhanden
        if self._electrical_production_data is not None:
            # füge aktuelle elektrische Produktion von Energie dem Speicher hinzu
            self._electrical_storage += float(self._electrical_production_data.pop(0)[1])
            # Konsolenausgabe, um aktuellen Stand nachvollziehen zu können
            print("  {} electrical storage: {:.3f}kWh".format(self.name, self._electrical_storage))
        # Elektrischer Verbrauch laden funktioniert nur, wenn noch Daten im Stack vorhanden
        if self._electrical_consumption_data is not None:
            # Elektrischen Verbrauch aus Stack laden.
            # Verbrauch ist vor diesem Schritt immer 0 (daher nicht +=),
            # da in jedem Zeitschritt über den Markt ausgeglichen wird
            self._total_electrical_consumption = self._electrical_consumption_data.pop(0)[2]
            # Konsolenausgabe, um aktuellen Stand nachvollziehen zu können
            print("  {} electrical consumption: {:.3f}kWh".format(self.name, self._total_electrical_consumption))

    # verarbeite elektrische Energie aus Eigenproduktion
    def electrical_self_consumption(self):
        # wenn der elektrische Speicher nicht leer ist und der elektrische Verbrauch nicht größer ist als der Speicher,
        # dann entnimm den aktuellen Verbrauch aus dem eigenen Speicher
        if self._electrical_storage > 0 and self._electrical_storage >= self._total_electrical_consumption:
            self._electrical_storage -= self._total_electrical_consumption
        else:
            # wenn nicht genüügend elektrische Energie im eigenen Speicher vorhanden,
            # dann speichere wie viel elektrische Energie am Markt angefragt werden muss
            self._electricity_to_request = self._total_electrical_consumption - self._electrical_storage
            # In diesem Szenario ist der eigene elektrische Speicher immer 0,
            # da wir so viel wie möglich eigene Energie nutzen wollen
            self._electrical_storage = 0
        # wenn elektrische Energie nach dem Eigenverbrauch übrig ist,
        # können wir diese am Markt anbieten
        self._offered_electrical_power = self._electrical_storage

    # wenn wir elektrische Energie benötigt wird, da wir nichts im eigenen Speicher haben,
    # dann müssen wir diese übrige Menge am Markt anfragen
    def purchase_electricity_on_market(self):
        if self._electricity_to_request > 0:
            self._market.request_electrical_energy(self, self._electricity_to_request)

    # siehe "load_electricity_step_data" nur mit thermischer Energie
    def load_thermal_step_data(self):
        if self._thermal_production_data is not None:
            self._thermal_storage += float(self._thermal_production_data.pop(0)[1])
            print("  {} thermal storage: {}l".format(self.name, self._thermal_storage))

        if self._thermal_consumption_data is not None:
            self._total_thermal_consumption = self._thermal_consumption_data.pop(0)[2]
            print("  {} thermal consumption: {}l".format(self.name, self._total_thermal_consumption))

    # siehe "electrical_self_consumption" nur mit thermischer Energie
    def thermal_self_consumption(self):
        if self._thermal_storage > 0 and self._thermal_storage >= self._total_thermal_consumption:
            self._thermal_storage -= self._total_thermal_consumption
        else:
            # deplete current electrical storage
            self._thermal_energy_to_request = self._total_thermal_consumption - self._thermal_storage
            self._thermal_storage = 0
        # set amount to offer on marketplace
        self._offered_thermal_power = self._thermal_storage

    # siehe "purchase_electricity_on_market" nur mit thermischer Energie
    def purchase_thermal_energy_on_market(self):
        if self._thermal_energy_to_request > 0:
            self._market.request_thermal_energy(self, self._thermal_energy_to_request)



