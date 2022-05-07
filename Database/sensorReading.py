
class SensorReading():
    def __init__(self,sensorID, temperature, humidity, pm10, pm25, no2, co):
        self.sensorID = sensorID
        self.temperature = temperature
        self.humidity = humidity
        self.pm10 = pm10
        self.pm25 = pm25
        self.no2 = no2
        self.co = co
