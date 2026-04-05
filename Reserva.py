import mysql.connector
from conexao import obter_conexao

class Reserva:

    def __init__(self, id_reserva, cliente_nome, suite_numero, date_in, date_out, status):
        self.id = id_reserva
        self.cliente_nome = cliente_nome
        self.suite_numero = suite_numero
        self.date_in = date_in
        self.date_out = date_out
        self.status = status

    @staticmethod
    def carregar_todas():
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM reservas")
            return [
                Reserva(
                    r["id"],
                    r["cliente_nome"],
                    r["suite_numero"],
                    r["date_in"],
                    r["date_out"],
                    r["status"],
                )
                for r in cursor.fetchall()
            ]
        except mysql.connector.Error:
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def registrar_checkin(cliente_nome, suite_numero, date_in, date_out):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO reservas (cliente_nome, suite_numero, date_in, date_out, status) VALUES (%s, %s, %s, %s, 'Ativa')"
            cursor.execute(sql, (cliente_nome, suite_numero, date_in, date_out))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            conn.close()

    def registrar_checkout(self):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            sql = "UPDATE reservas SET status = 'Finalizada' WHERE id = %s"
            cursor.execute(sql, (self.id,))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            conn.close()