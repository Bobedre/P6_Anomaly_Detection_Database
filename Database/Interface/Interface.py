import json
import logging
import time

from signalrcore.hub_connection_builder import HubConnectionBuilder
from DataHandler.DBConnection import DBConnection


class Interface:

    def connectToHub(self):
        dbconnection = DBConnection()
        print("Connected to DB")

        self.hub_connection = HubConnectionBuilder()\
            .with_url("http://localhost:8081/suggestorHub")\
            .with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                })\
            .configure_logging(logging.DEBUG)\
            .build()
        self.hub_connection.on_open(lambda: self.onConnection())
        self.hub_connection.on_close(lambda: print("connection closed"))
        self.hub_connection.on("RetrieveReadings", self.RetrieveReadings(dbconnection))
        self.hub_connection.on("StoreReadings", self.StoreSensorReading(dbconnection))
        self.hub_connection.start()

        while not self.end:
            time.sleep(1)

        self.hub_connection.stop()

    def onConnection(self):
        print("connection opened and handshake received ready to send messages")
        self.hub_connection.send("DBJoin", [])


    def RetrieveReadings(self, dbconnection):
        result = dbconnection.retrieveData()
        self.sendResultToHub(result)

    def StoreSensorReadings(self, dbconnection):
        dbconnection.storeData()


    def sendResultToHub(self, result):
        json_dump = json.dumps(result)
        self.hub_connection.send("ProbeReadingFromDB", json_dump)
        print("result send")
