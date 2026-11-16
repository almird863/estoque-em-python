import sqlite3

connect = sqlite3.connect('estoque.db')
cursor = connect.cursor()

#####################################################################
#                             CRIAR
#####################################################################

def criar_tabela():
    cursor.execute('''CREATE TABLE IF NOT EXISTS Estoque (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade INTEGER NOT NULL
                        )''')
    connect.commit()


#####################################################################
#                             INSERIR
#####################################################################


def inserir_item(nome, qnt):
    try:
        cursor.execute('''INSERT INTO Estoque (nome, quantidade)
                            VALUES (?, ?)''', (nome, qnt))
        connect.commit()

        return True, "Item inserido com sucesso."

    except sqlite3.Error as e:

        return False, f"Erro ao inserir item: {e}"


#####################################################################
#                             BUSCAR
#####################################################################


def listar_items():
    try:
        cursor.execute("SELECT * FROM Estoque")

        return True, cursor.fetchall()
    
    except sqlite3.Error as e:
        print(e)

        return False, None


def buscar_item_por_nome(nome):
    try:
        cursor.execute("SELECT * FROM Estoque WHERE nome = ?", (nome,))

        return True, cursor.fetchone()

    except sqlite3.Error as e:
        print(e)

        return False, None


def buscar_item_por_quantidade_menor_que(qnt):
    try:
        cursor.execute("SELECT * FROM Estoque WHERE quantidade < ?", (qnt,))

        return True, cursor.fetchall()

    except sqlite3.Error as e:
        print(e)

        return False, None

    
def buscar_item_por_quantidade_maior_que(qnt):
    try:
        cursor.execute("SELECT * FROM Estoque WHERE quantidade > ?", (qnt,))

        return True, cursor.fetchall()

    except sqlite3.Error as e:
        print(e)

        return False, None


#####################################################################
#                            ATUALIZAR
#####################################################################


def atualizar_quantidade(qnt, id):
    try:
        cursor.execute('''UPDATE OR REPLACE Estoque
                            SET quantidade = ?
                            WHERE id = ?''', (qnt, id))
        connect.commit()

        return True, "Item atualizado com sucesso."

    except sqlite3.Error as e:

        return False, f"Erro ao atualizar o item: {e}"


#####################################################################
#                             DELETAR
#####################################################################


def excluir_item(id):
    try:
        cursor.execute("DELETE FROM Estoque WHERE id = ?", (id,))
        connect.commit()

        return True, "Item deletado com sucesso"

    except sqlite3.Error as e:

        return False, f"Erro ao deletar o item: {e}"