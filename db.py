import sqlite3

def consulta(comando):
    """ Comando para consultar informações da base de dados. """
    conn = sqlite3.connect('bancodedados.db')
    cursor = conn.cursor()
    cursor.execute(comando)
    recset = cursor.fetchall()
    conn.close()
    return recset

def inclusao(comando):
    """ Comando para incluir instruções de upload e exclução de dados. """
    conn = sqlite3.connect('bancodedados.db')
    cursor = conn.cursor()
    cursor.execute(comando)
    conn.commit()
    conn.close()