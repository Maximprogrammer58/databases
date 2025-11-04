import mysql.connector


class RawRepository:
    def __init__(self, conn: mysql.connector.connection.MySQLConnection, table_name, columns, pk):
        self.conn = conn
        self.table_name = table_name
        self.columns = columns
        self.pk = pk

    def get_all(self):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM {self.table_name}")
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_by_id(self, _id):
        cursor = self.conn.cursor(dictionary=True)
        sql = f"SELECT * FROM {self.table_name} WHERE {self.pk}=%s"
        cursor.execute(sql, (_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def add(self, values: tuple):
        cursor = self.conn.cursor()
        placeholders = ",".join(["%s"]*len(values))
        cols = ",".join(self.columns)
        sql = f"INSERT INTO {self.table_name} ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        self.conn.commit()
        cursor.close()
        return cursor.lastrowid

    def update(self, _id, values: dict):
        cursor = self.conn.cursor()
        set_expr = ",".join([f"{k}=%s" for k in values.keys()])
        sql = f"UPDATE {self.table_name} SET {set_expr} WHERE {self.pk}=%s"
        cursor.execute(sql, tuple(values.values()) + (_id,))
        self.conn.commit()
        cursor.close()

    def delete(self, _id):
        cursor = self.conn.cursor()
        sql = f"DELETE FROM {self.table_name} WHERE {self.pk}=%s"
        cursor.execute(sql, (_id,))
        self.conn.commit()
        cursor.close()
