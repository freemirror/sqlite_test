import sqlite3
import matplotlib.pyplot as plt
import numpy as np


conn = sqlite3.connect('flights.db')
cur = conn.cursor()

cur.execute("""SELECT COUNT(id_runway) as summa, strftime('%m', landing_dt)
FROM runways
LEFT JOIN flights ON runway_id=id_runway
GROUP BY strftime('%m', landing_dt)
;""")

data = cur.fetchall()

X = []
Y = []

for count in range(len(data)):
    Y.append(data[count][0])
    X.append(data[count][1])

Y1 = np.full(np.size(Y), np.mean(Y))
Y2 = np.full(np.size(Y), 390)

plt.plot(X, Y, 'b--', linewidth=2)
plt.plot(X, Y1, 'r-')
plt.plot(X, Y2, 'g')
plt.show()

cur.execute("""SELECT COUNT(*), cast((julianday(leaving_dt) - julianday(landing_dt)) *1000 as int)
FROM flights
GROUP BY (cast((julianday(leaving_dt) - julianday(landing_dt)) *1000 as int)); """)

data2 = cur.fetchall()

index = []
nums = []
for i in range(1, len(data2)):
    nums.append(data2[i][0])
    index.append(data2[i][1])

plt.bar(index, nums)
plt.show()

series1 = []

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Airbus A310' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series1.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Airbus A310' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series1.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Airbus A310' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series1.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Airbus A310' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series1.append(cur.fetchone())

series2 = []

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Saab' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series2.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Saab' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series2.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Saab' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series2.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Saab' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series2.append(cur.fetchone())

series3 = []

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Bombardier Dash 8' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series3.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Bombardier Dash 8' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series3.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Bombardier Dash 8' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series3.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='Bombardier Dash 8' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series3.append(cur.fetchone())

series4 = []

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='ATR 42/72' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series4.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='ATR 42/72' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series4.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='ATR 42/72' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series4.append(cur.fetchone())

cur.execute("""SELECT COUNT(model)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE model='ATR 42/72' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series4.append(cur.fetchone())

ser1 = []
ser2 = []
ser3 = []
ser4 = []
for i in range(4):
    ser1.append(series1[i][0])
    ser2.append(series2[i][0])
    ser3.append(series3[i][0])
    ser4.append(series4[i][0])

index = np.arange(4)
plt.title('Соотношение моделей самолетов на рейсах по кварталам')
plt.bar(index, ser1, color='r')
plt.bar(index, ser2, color='b', bottom=np.array(ser1))
plt.bar(index, ser3, color='k', bottom=(np.array(ser1) + np.array(ser2)))
plt.bar(index, ser4, color='c', bottom=(np.array(ser1) + np.array(ser2) + np.array(ser3)))
plt.xticks(index, ['1 квартал', '2 квартал', '3 квартал', '4 квартал'])
plt.show()

series5 = []

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Баку' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series5.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Баку' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series5.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Баку'  AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series5.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Баку' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series5.append(cur.fetchone())

series6 = []

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Мельбурн' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series6.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Мельбурн' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series6.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Мельбурн' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series6.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Мельбурн' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series6.append(cur.fetchone())

series7 = []

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Джакарта' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series7.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Джакарта' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series7.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Джакарта' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series7.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Джакарта' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series7.append(cur.fetchone())

series8 = []

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Берлин' AND strftime('%m', landing_dt) BETWEEN '0' AND '03'
""")
series8.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Берлин' AND strftime('%m', landing_dt) BETWEEN '04' AND '06'
""")
series8.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Берлин' AND strftime('%m', landing_dt) BETWEEN '07' AND '09'
""")
series8.append(cur.fetchone())

cur.execute("""SELECT SUM(seats)
FROM flights
LEFT JOIN planes ON flight_id=id_flight
WHERE departure='Берлин' AND strftime('%m', landing_dt) BETWEEN '10' AND '12'
""")
series8.append(cur.fetchone())

ser5 = []
ser6 = []
ser7 = []
ser8 = []
for i in range(4):
    ser5.append(series5[i][0])
    ser6.append(series6[i][0])
    ser7.append(series7[i][0])
    ser8.append(series8[i][0])

index = np.arange(4)
bw = 0.2
plt.title('A Multiseries Bar Chart', fontsize=20)
plt.bar(index, ser5, bw, color='r')
plt.bar(index + bw, ser6, bw, color='b')
plt.bar(index + 2 * bw, ser7, bw, color='k')
plt.bar(index + 3 * bw, ser8, bw, color='c')
plt.xticks(index + 2 * bw, ['1 квартал', '2 квартал', '3 квартал', '4 квартал'])
plt.show()

labels = []
values = []

cur.execute("""SELECT departure, COUNT(flight_id)
FROM runways
LEFT JOIN flights ON runway_id=id_runway
WHERE sum=(SELECT MAX(sum) FROM runways)
GROUP BY departure
""")

data3 = cur.fetchall()

for i in range(len(data3)):
    labels.append(data3[i][0])
    values.append(data3[i][1])

explode = np.zeros_like(values, dtype=np.float64)
explode[6] = 0.3
plt.title('Доля ' + labels[6] + ' на взлетнопосадочную полосу')
plt.pie(values, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.show()
