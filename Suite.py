import mysql.connector
from conexao import obter_conexao

class Suite:

    def __init__(self, numero, tipo, preco):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco

    @staticmethod
    def carregar_todas():
        """Retorna uma lista de OBJETOS Suite."""
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM suites")
            return [
                Suite(r["numero"], r["tipo"], r["preco"])
                for r in cursor.fetchall()
            ]
        except mysql.connector.Error:
            return []
        finally:
            cursor.close()
            conn.close()