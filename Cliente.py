import mysql.connector
from conexao import obter_conexao

class Cliente:

    def __init__(self, id_cliente, nome, telefone, email):
        self.id = id_cliente
        self.nome = nome
        self.telefone = telefone
        self.email = email

    @staticmethod
    def carregar_todos():
        conn = obter_conexao()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM clientes")
            return [
                Cliente(r["id"], r["nome"], r["telefone"], r["email"])
                for r in cursor.fetchall()
            ]
        except mysql.connector.Error:
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def cadastrar(nome, telefone, email):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            sql = "INSERT INTO clientes (nome, telefone, email) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, telefone, email))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            conn.close()

    def atualizar(self, novo_nome, novo_tel, novo_email):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            sql = "UPDATE clientes SET nome = %s, telefone = %s, email = %s WHERE id = %s"
            cursor.execute(sql, (novo_nome, novo_tel, novo_email, self.id))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            conn.close()

    def deletar(self):
        conn = obter_conexao()
        cursor = conn.cursor()
        try:
            sql = "DELETE FROM clientes WHERE id = %s"
            cursor.execute(sql, (self.id,))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            cursor.close()
            conn.close()