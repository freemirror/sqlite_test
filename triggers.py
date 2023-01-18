import sqlite3


conn = sqlite3.connect('flights.db')

cur = conn.cursor()

cur.execute(""" CREATE TABLE IF NOT EXISTS log_In_runways(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TABLE IF NOT EXISTS log_In_flights(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TABLE IF NOT EXISTS log_In_planes(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_RInA AFTER INSERT
            ON runways
            BEGIN
            INSERT
              INTO log_In_runways(Id_cust, date, trig_type)
              VALUES (NEW.runway_id, datetime('now'), 'ins_rw_af');
            END;""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_FInA AFTER INSERT
            ON flights
            BEGIN
            INSERT
              INTO log_In_flights(Id_cust, date, trig_type)
              VALUES (NEW.flight_id, datetime('now'),'ins_fl_af');
            END;""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_PInA AFTER INSERT
            ON planes
            BEGIN
            INSERT
              INTO log_In_planes(Id_cust, date, trig_type)
              VALUES (NEW.airplane_id, datetime('now'),'ins_pl_af');
            END;""")
conn.commit()

cur.execute("""INSERT
                 INTO runways(length, bearing)
                 VALUES ('6.5','160');""")
conn.commit()

cur.execute("""INSERT
                 INTO flights(name, landing_dt, leaving_dt, departure, id_runway)
                 VALUES ('FT 857','2022-04-16 00:23:27', '2022-04-16 00:42:27', 'Баку', 10);""")
conn.commit()

cur.execute("""INSERT
                 INTO planes(model, seats, length, factory_num, id_flight)
                 VALUES ('Airbus A320', 214, 44.9, 39317066, 5001);""")
conn.commit()

print('Лог добавления новых записей')

cur.execute("SELECT * FROM log_In_runways")
print(cur.fetchall())

cur.execute("SELECT * FROM log_In_flights")
print(cur.fetchall())

cur.execute("SELECT * FROM log_In_planes")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Del_runways(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Del_flights(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Del_planes(
            Id_cust INTEGER NOT NULL,
            date TEXT NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_RDelA AFTER DELETE
            ON runways
            BEGIN
            INSERT
              INTO log_Del_runways(Id_cust, date, trig_type)
              VALUES (OLD.runway_id, datetime('now'), 'del_rw_af');
            END;""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_FDelA AFTER DELETE
            ON flights
            BEGIN
            INSERT
              INTO log_Del_flights(Id_cust, date, trig_type)
              VALUES (OLD.flight_id, datetime('now'), 'del_fl_af');
            END;""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_PDelA AFTER DELETE
            ON planes
            BEGIN
            INSERT
              INTO log_Del_planes(Id_cust, date, trig_type)
              VALUES (OLD.airplane_id, datetime('now'), 'del_pl_af');
            END;""")
conn.commit()

cur.execute("DELETE FROM runways WHERE runway_id = 10;")
conn.commit()

cur.execute("DELETE FROM flights WHERE flight_id = 5001;")
conn.commit()

cur.execute("DELETE FROM planes WHERE airplane_id = 5001;")
conn.commit()

print('Лог удаления старых записей')

cur.execute("SELECT * FROM log_Del_runways")
print(cur.fetchall())

cur.execute("SELECT * FROM log_Del_flights")
print(cur.fetchall())

cur.execute("SELECT * FROM log_Del_planes")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Upd_flights(
            Id_flight INTEGER NOT NULL,
            old_name TEXT NOT NULL,
            new_name TEXT NOT NULL,
            old_landing_dt DATETIME NOT NULL,
            new_landing_dt DATETIME NOT NULL,
            old_leaving_dt DATETIME NOT NULL,
            new_leaving_dt DATETIME NOT NULL,
            old_eparture TEXT NOT NULL,
            new_departure TEXT NOT NULL,
            old_id_runway INTEGER,
            new_id_runway INTEGER,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_Upd_flight AFTER UPDATE
            ON flights
            BEGIN
            INSERT
              INTO log_Upd_flights(
              Id_flight,
              old_name,
              new_name,
              old_landing_dt,
              new_landing_dt,
              old_leaving_dt,
              new_leaving_dt,
              old_eparture,
              new_departure,
              old_id_runway,
              new_id_runway,
              trig_type)
              VALUES (
              OLD.flight_id,
              OLD.name,
              NEW.name,
              OLD.landing_dt,
              NEW.landing_dt,
              OLD.leaving_dt,
              NEW.leaving_dt,
              OLD.departure,
              NEW.departure,
              OLD.id_runway,
              NEW.id_runway,
              'any_update');
            END;""")
conn.commit()

cur.execute("""UPDATE flights SET name = 'KX 459'
            WHERE flight_id = 1;""")
conn.commit()

cur.execute("""UPDATE flights SET landing_dt = '2022-07-17 18:18:28'
            WHERE flight_id = 1;""")
conn.commit()

cur.execute("""UPDATE flights SET leaving_dt = '2022-07-17 18:56:28'
            WHERE flight_id = 1;""")
conn.commit()

cur.execute("""UPDATE flights SET departure = 'Париж'
            WHERE flight_id = 1;""")
conn.commit()

cur.execute("""UPDATE flights SET id_runway = 2
            WHERE flight_id = 1;""")
conn.commit()

print('Лог внесения любых изменений в таблицу рейсов')

cur.execute("SELECT * FROM log_Upd_flights")
for elem in cur.fetchall():
    print(elem)

print('\n', '*' * 100, '\n')

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Upd_runways(
            Id_runway INTEGER NOT NULL,
            old_length REAL NOT NULL,
            new_length REAL NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_Upd_runways_length AFTER UPDATE
            OF length
            ON runways
            BEGIN
            INSERT
              INTO log_Upd_runways(Id_runway, old_length, new_length, trig_type)
              VALUES (OLD.runway_id, OLD.length, NEW.length, 'upd_length');
            END;""")
conn.commit()

cur.execute("""UPDATE runways SET length = 10.1
            WHERE runway_id = 1;""")
conn.commit()

cur.execute("""UPDATE runways SET bearing = 250
            WHERE runway_id = 1;""")
conn.commit()

print('Лог изменения длинны взлетнопосадочной полосы')

cur.execute("SELECT * FROM log_Upd_runways")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute(""" CREATE TABLE IF NOT EXISTS log_Con_runways(
            Id_runway INTEGER NOT NULL,
            old_length REAL NOT NULL,
            new_length REAL NOT NULL,
            trig_type TEXT)""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS log_UpdCondition AFTER UPDATE
            ON runways WHEN (OLD.length - NEW.length) > 0
            BEGIN
            INSERT
              INTO log_Con_runways(Id_runway, old_length, new_length, trig_type)
              VALUES (OLD.runway_id, OLD.length, NEW.length, 'condition_update');
            END;""")
conn.commit()

cur.execute("""UPDATE runways SET length = 11.1
            WHERE runway_id = 1;""")
conn.commit()

cur.execute("""UPDATE runways SET length = 8.1
            WHERE runway_id = 1;""")
conn.commit()

print('Лог уменьшения длинны взлетнопосадочной полосы')

cur.execute("SELECT * FROM log_Con_runways")
print(cur.fetchall())

print('\n', '*' * 100, '\n')

cur.execute("""INSERT
                 INTO runways(length, bearing)
                 VALUES ('6.5','160');""")
conn.commit()

cur.execute("""INSERT
                 INTO flights(name, landing_dt, leaving_dt, departure, id_runway)
                 VALUES ('FF 000','2022-04-16 00:23:27', '2022-04-16 00:42:27', 'Баку', 11);""")
conn.commit()

cur.execute("""INSERT
                 INTO flights(name, landing_dt, leaving_dt, departure, id_runway)
                 VALUES ('TT 000','2022-04-16 05:23:27', '2022-04-16 05:42:27', 'Париж', 11);""")
conn.commit()

cur.execute("""INSERT
                 INTO planes(model, seats, length, factory_num, id_flight)
                 VALUES ('Airbus A320', 214, 44.9, 00000000, 5002);""")
conn.commit()

cur.execute("""INSERT
                 INTO planes(model, seats, length, factory_num, id_flight)
                 VALUES ('Saab', 120, 25.9, 11111111, 5003);""")
conn.commit()

print('Данные для каскадного удаления')

cur.execute("""SELECT * FROM runways
                WHERE runway_id = 11""")
print(cur.fetchall())

cur.execute("""SELECT * FROM flights
                WHERE flight_id > 5000""")
print(cur.fetchall())

cur.execute("""SELECT * FROM planes
                WHERE airplane_id > 5000""")
print(cur.fetchall())

print('\n', '*' * 20, '\n')

cur.execute(""" CREATE TRIGGER IF NOT EXISTS cas_del_fl
            BEFORE DELETE
            ON runways
            BEGIN
            DELETE FROM flights WHERE flights.id_runway = OLD.runway_id;
            END;""")
conn.commit()

cur.execute(""" CREATE TRIGGER IF NOT EXISTS cas_del_pl
            BEFORE DELETE
            ON flights
            BEGIN
            DELETE FROM planes WHERE planes.id_flight = OLD.flight_id;
            END;""")
conn.commit()

cur.execute("DELETE FROM runways WHERE runway_id = 11;")
conn.commit()

print('Проверка данных после каскадного удаления')

cur.execute("""SELECT * FROM runways
                WHERE runway_id = 11""")
print(cur.fetchall())

cur.execute("""SELECT * FROM flights
                WHERE flight_id > 5000""")
print(cur.fetchall())

cur.execute("""SELECT * FROM planes
                WHERE airplane_id > 5000""")
print(cur.fetchall())
