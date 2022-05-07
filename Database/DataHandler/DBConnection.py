import pyodbc as pyo
from sensorReading import SensorReading

class DBConnection():
    def __init__(self):

        self.connection = pyo.connect('Driver={ODBC Driver 18 for SQL Server};'
                                 'Server=(localdb)\MSSQLLocalDB;'
                                 'Database=SensorReadings;'
                                 'Trusted_Connection=yes;')

        self.curser = self.connection.cursor()

    def storeData(self, values):
        insertQuery = '''
                INSERT INTO dbo.sensorReadings (sensorID, temperature, humidity, pm10, pm25, no2, co)
                VALUES
                (?, ?, ?, ?, ?, ?, ?)
                '''

        self.curser.execute(insertQuery, values)
        print("Inserted!")
        self.connection.commit()

    def retrieveData(self):
        result = []

        self.curser.execute("""
                            select *
                            from dbo.sensorReadings
                           """)

        for row in self.curser:
            result.append(SensorReading(row.sensorID, row.temperature, row.humidity,
                                        row.pm10, row.pm25, row.no2, row.co))
        print("Retrieved!")
        return result

    def updateTemperature(self,value,sensorID):
        updateQuery = '''
                UPDATE dbo.sensorReadings
                SET temperature = ?
                WHERE sensorID = ?
                '''

        self.curser.execute(updateQuery,value,sensorID)

    def checkDriver(self):
        for driver in pyo.drivers():
            print(driver)



  #self.curser.execute("""
  #                          select *
  #                          from dbo.sensorReadings
  #                          where sensorID = ? """, sensorID) //If we have to retrieve a specific probe we need sensorID as parameter for the method
