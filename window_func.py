import sqlite3

conn = sqlite3.connect('flights.db')

cur = conn.cursor()

cur.execute("""SELECT
  dense_rank() OVER w AS rank,
  length, bearing, sum
FROM runways
WINDOW w AS (ORDER BY sum DESC)
ORDER BY sum DESC, length, runway_id;""")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  ntile(5) OVER w AS tile,
  model, length, seats, factory_num, id_flight
FROM planes
WINDOW w AS (ORDER BY seats)
ORDER BY seats;""")
print(cur.fetchall())


print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  dense_rank() OVER w AS rank,
  flight_id, name, landing_dt, leaving_dt, departure, seats,
  first_value(seats) OVER w AS top,
  last_value(seats) OVER w AS bottom
FROM flights, planes
WHERE flight_id = id_flight
WINDOW w AS (PARTITION BY departure
ORDER BY seats DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY departure, seats DESC, flight_id;""")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  dense_rank() OVER w AS rank,
  DATE(landing_dt), seats,
  lag(DATE(landing_dt), 1) OVER w1
FROM flights, planes
WHERE flight_id = id_flight
WINDOW w AS (PARTITION BY DATE(landing_dt)
ORDER BY seats DESC),
w1 AS (ORDER BY DATE(landing_dt))
ORDER BY DATE(landing_dt), seats DESC;""")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  DATE(landing_dt), seats,
  SUM(seats) OVER w AS summa,
  count(*) OVER w AS count_of_flight,
  round(seats * 100.0 / SUM(seats) over w) as percent
FROM flights, planes
WHERE flight_id = id_flight
WINDOW w AS (PARTITION BY DATE(landing_dt)
ORDER BY seats DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY DATE(landing_dt), seats DESC;""")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  DATE(landing_dt), length,
  MAX(length) OVER w AS maximum,
  round(AVG(length) OVER w) AS average_length,
  round(length * 100.0 / MAX(length) over w) as percent
FROM flights, planes
WHERE flight_id = id_flight
WINDOW w AS (PARTITION BY DATE(landing_dt)
ORDER BY length DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
ORDER BY DATE(landing_dt), length DESC;""")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""SELECT
  DATE(landing_dt), seats,
  SUM(seats) OVER w AS summa,
  count(*) OVER w AS count_of_flight,
  round(seats * 100.0 / SUM(seats) over w) as percent,
  round(seats * 100.0 / SUM(seats) over w1) as percent_cur
FROM flights, planes
WHERE flight_id = id_flight
WINDOW w AS (PARTITION BY DATE(landing_dt)
ORDER BY seats DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING),
w1 AS (PARTITION BY DATE(landing_dt)
ORDER BY seats DESC
ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
ORDER BY DATE(landing_dt), seats DESC;""")
print(cur.fetchall())
