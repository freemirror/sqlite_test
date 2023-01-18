import random
import sqlite3
import string
from csv import DictReader
from datetime import datetime, timedelta

from planes import PLANES


def random_datetime():
    start_date = datetime.strptime('2022-1-1 00:00:00', FORMAT)
    end_date = datetime.strptime('2022-12-31 23:59:00', FORMAT)
    delta = start_date + random.random() * (end_date - start_date)
    delta_leaving = delta + timedelta(minutes=random.randint(15, 25))
    landing_dt = datetime.strftime(delta, FORMAT)
    leaving_dt = datetime.strftime(delta_leaving, FORMAT)
    return landing_dt, leaving_dt


FORMAT = '%Y-%m-%d %H:%M:%S'
CITIES = []

cities_file = open('cities.csv', encoding="utf-8")
for row in DictReader(cities_file):
    CITIES.append(row['Город'])

conn = sqlite3.connect('flights.db')

cur = conn.cursor()

cur.execute("PRAGMA foreign_keys=ON")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS runways(
   runway_id INTEGER PRIMARY KEY AUTOINCREMENT,
   length REAL NOT NULL,
   bearing INTEGER NOT NULL,
   sum INTEGER NOT NULL DEFAULT 0);
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS flights(
   flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL,
   landing_dt DATETIME NOT NULL,
   leaving_dt DATETIME NOT NULL,
   departure TEXT NOT NULL,
   id_runway INTEGER,
   FOREIGN KEY (id_runway) REFERENCES runways(runway_id));
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS planes(
  airplane_id INTEGER PRIMARY KEY AUTOINCREMENT,
  model TEXT NOT NULL,
  seats INTEGER NOT NULL,
  length REAL NOT NULL,
  factory_num INTEGER NOT NULL,
  id_flight INTEGER,
  FOREIGN KEY (id_flight) REFERENCES flights(flight_id));
""")
conn.commit()


runways = []
for count in range(1, 10):
    length = round(random.uniform(0.250, 12.000), 3)
    bearing = random.randint(10, 360) // 10 * 10
    tup = (length, bearing)
    runways.append(tup)

cur.executemany("INSERT INTO runways(length, bearing) VALUES (?,?)", runways)
conn.commit()

flights = []
for count in range(5000):
    name = (random.choice(string.ascii_uppercase)
            + random.choice(string.ascii_uppercase) + ' '
            + str(random.randint(100, 999)))
    landing_dt, leaving_dt = random_datetime()
    departure = random.choice(CITIES)
    id_runway = random.randint(1, 9)
    tup = (name, landing_dt, leaving_dt, departure, id_runway)
    flights.append(tup)

cur.executemany("INSERT INTO flights(name, landing_dt, leaving_dt, departure, id_runway) VALUES (?,?,?,?,?)", flights)
conn.commit()

planes = []
for count in range(5000):
    model = random.choice(PLANES)
    seats = random.randint(100, 350)
    length = round(random.uniform(30.0, 80.0), 1)
    factory_num = random.randint(10000000, 99999999)
    id_flight = count + 1
    tup = (model, seats, length, factory_num, id_flight)
    planes.append(tup)

cur.executemany("INSERT INTO planes(model, seats, length, factory_num, id_flight) VALUES (?,?,?,?,?)", planes)
conn.commit()

cur.execute(""" UPDATE runways
  SET sum = (SELECT COUNT(id_runway)
  FROM flights
  WHERE runways.runway_id=flights.id_runway)
""")
conn.commit()
