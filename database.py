import mysql.connector
from conexao import obter_conexao

def inicializar_banco():
    """Cria as tabelas necessárias caso elas não existam no MySQL."""
    conn = mysql.connector.connect(
        host="localhost", user="root", password=""
    )
    cursor = conn.cursor()

    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS hotel_db")
        cursor.execute("USE hotel_db")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20),
                email VARCHAR(100)
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS suites (
                numero INT PRIMARY KEY,
                tipo VARCHAR(50) NOT NULL,
                preco DECIMAL(10, 2) NOT NULL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reservas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cliente_nome VARCHAR(100) NOT NULL,
                suite_numero INT NOT NULL,
                date_in DATE NOT NULL,
                date_out DATE NOT NULL,
                status VARCHAR(20) DEFAULT 'Ativa'
            )
        """
        )

        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao inicializar o banco: {err}")
    finally:
        cursor.close()
        conn.close()

inicializar_banco()