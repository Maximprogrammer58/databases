class RawSQLService:
    def __init__(self, conn):
        self.conn = conn

    def query1_flights_from_airport(self, airport_name):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT a_dep.title AS departure_airport,
               a_arr.title AS arrival_airport,
               am.model_title,
               f.departure_date,
               f.arrival_date
        FROM flights f
        JOIN airports a_dep ON f.departure_port_id = a_dep.port_id
        JOIN airports a_arr ON f.arrival_port_id = a_arr.port_id
        JOIN aircraft_models am ON f.model_id = am.model_id
        WHERE a_dep.title=%s
        """
        cursor.execute(sql, (airport_name,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def query2_flight_counts(self, year):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT a.title AS airport_name,
               COUNT(f.flight_id) AS count
        FROM airports a
        LEFT JOIN flights f ON a.port_id = f.departure_port_id AND YEAR(f.departure_date) = %s
        GROUP BY a.port_id, a.title
        ORDER BY count DESC
        """
        cursor.execute(sql, (year,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def query3_top_booked_flights(self):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT d.title AS departure_airport,
               a.title AS arrival_airport,
               f.departure_date,
               COUNT(b.booking_id) AS count
        FROM bookings b
        JOIN flights f ON b.flight_id = f.flight_id
        JOIN airports d ON f.departure_port_id = d.port_id
        JOIN airports a ON f.arrival_port_id = a.port_id
        GROUP BY d.title, a.title, f.departure_date
        ORDER BY count DESC
        LIMIT 5
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query4_customers_with_many_bookings(self, min_bookings):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT c.first_name,
               c.last_name,
               COUNT(b.booking_id) AS count
        FROM customers c
        JOIN bookings b ON c.customer_id = b.customer_id
        GROUP BY c.customer_id, c.first_name, c.last_name
        HAVING COUNT(b.booking_id) > %s
        ORDER BY c.last_name, c.first_name
        """
        cursor.execute(sql, (min_bookings,))
        result = cursor.fetchall()
        cursor.close()
        return result

    def query5_flights_with_max_bookings(self):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT f.flight_id
        FROM flights f
        JOIN bookings b ON f.flight_id = b.flight_id
        GROUP BY f.flight_id
        HAVING COUNT(b.booking_id) = (
            SELECT MAX(cnt)
            FROM (
                SELECT COUNT(b2.booking_id) AS cnt
                FROM bookings b2
                GROUP BY b2.flight_id
            ) AS sub
        )
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query6_booking_statistics(self):
        cursor = self.conn.cursor(dictionary=True)
        sql = """
        SELECT ap.title AS departure_airport,
               COALESCE(MIN(cnt),0) AS min,
               COALESCE(AVG(cnt),0) AS avg,
               COALESCE(MAX(cnt),0) AS max
        FROM airports ap
        LEFT JOIN (
            SELECT f.departure_port_id, COUNT(b.booking_id) AS cnt
            FROM flights f
            LEFT JOIN bookings b ON f.flight_id = b.flight_id
            GROUP BY f.flight_id, f.departure_port_id
        ) AS flight_stats ON ap.port_id = flight_stats.departure_port_id
        GROUP BY ap.port_id, ap.title
        """
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result
