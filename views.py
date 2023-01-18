import sqlite3


conn = sqlite3.connect('flights.db')

cur = conn.cursor()

cur.execute("""CREATE VIEW IF NOT EXISTS small_planes AS
            SELECT * FROM planes
            WHERE planes.seats < (SELECT 110 FROM planes)""")
conn.commit()

cur.execute("SELECT * FROM small_planes")
print(cur.fetchall())

cur.execute("SELECT COUNT(airplane_id) FROM small_planes")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""CREATE VIEW IF NOT EXISTS flights_with_sp AS
               SELECT * FROM flights, small_planes
               WHERE flights.flight_id =  small_planes.id_flight""")
conn.commit()

cur.execute("SELECT * FROM flights_with_sp")
print(cur.fetchall())

cur.execute("SELECT COUNT(flight_id) FROM flights_with_sp")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute(""" CREATE VIEW IF NOT EXISTS flights_with_sp_lim AS
            SELECT
              flights.flight_id AS flights_num,
              small_planes.model AS model_plane
            FROM flights, small_planes
            WHERE flights.flight_id = small_planes.id_flight
            LIMIT 10""")
conn.commit()

cur.execute("SELECT * FROM flights_with_sp_lim")
result = cur.fetchall()
id_from_lim_sel = result[0][0]
print(result)

print('\n', '*' * 100, '\n')

cur.execute("""CREATE TRIGGER IF NOT EXISTS upd_model
            INSTEAD OF UPDATE OF model_plane
            ON flights_with_sp_lim
            BEGIN
            UPDATE planes SET model = NEW.model_plane
            WHERE planes.id_flight = NEW.flights_num;
            END;""")
conn.commit()

cur.execute(f"UPDATE flights_with_sp_lim SET model_plane = 'Airbus A340-100'"
            f"WHERE flights_num = {id_from_lim_sel}")
conn.commit()

cur.execute(f"SELECT * FROM flights_with_sp_lim")
print(cur.fetchall())

cur.execute(f"SELECT * FROM planes WHERE airplane_id = {id_from_lim_sel}")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""CREATE TRIGGER IF NOT EXISTS del_plane
            INSTEAD OF DELETE
            ON flights_with_sp_lim
            BEGIN
            DELETE FROM planes
            WHERE planes.id_flight = OLD.flights_num;
            END;""")
conn.commit()

cur.execute(f"DELETE FROM flights_with_sp_lim "
            f"WHERE flights_num = {id_from_lim_sel};")
conn.commit()

cur.execute(f"SELECT * FROM flights_with_sp_lim "
            f"WHERE flights_num = {id_from_lim_sel}")
print(cur.fetchall())

cur.execute(f"SELECT * FROM planes WHERE airplane_id = {id_from_lim_sel}")
print(cur.fetchall())
