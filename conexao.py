import mysql.connector

def obter_conexao():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root", 
        database="hotel",
    )