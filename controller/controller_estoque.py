from models.model_estoque import (buscar_item_por_nome,
                                  atualizar_quantidade,
                                  excluir_item,
                                  inserir_item)


########################################################################
#                         CADASTRAR PRODUTO
########################################################################


def cadastrar_produto(nome, qnt):

    nome_item = nome.lower().strip()

    if not nome_item:
        return False, "Nome precisa ser válido"
    
    try:
        quantidade = int(qnt)
    except (ValueError, TypeError):
        return False, "Quantidade precisa ser um número inteiro"

    if quantidade <= 0:
        return False, "Quantidade precisa ser maior que zero."

    return inserir_item(nome_item, quantidade)


########################################################################
#                          ATUALIZAR PRODUTO
########################################################################

def somar_qnt_produto(nome, qnt):

    nome_item = nome.lower().strip()

    if not nome_item:
        return False, "Nome precisa ser válido"
    
    try:
        quantidade = int(qnt)
    except (ValueError, TypeError):
        return False, "Quantidade precisa ser um número inteiro"

    if quantidade <= 0:
        return False, "Quantidade adicionada precisa ser maior que zero."

    resposta, dados = buscar_item_por_nome(nome_item)

    if not resposta:
        return False, dados
    
    item_id, item_nome, item_qnt = dados[:3]

    item_qnt += quantidade

    return atualizar_quantidade(item_qnt, item_id)


def subtrair_qnt_produto(nome, qnt):

    nome_item = nome.lower().strip()

    if not nome_item:
        return False, "Nome precisa ser válido"
    
    try:
        quantidade = int(qnt)
    except (ValueError, TypeError):
        return False, "Quantidade precisa ser um número inteiro"

    if quantidade <= 0:
        return False, "Quantidade adicionada precisa ser maior que zero."

    resposta, dados = buscar_item_por_nome(nome_item)

    if not resposta:
        return False, dados
    
    item_id, item_nome, item_qnt = dados[:3]

    if quantidade >= item_qnt:
        return False, f"Estoque insuficiente: (Disponível: {item_qnt})"

    item_qnt -= quantidade
    
    return atualizar_quantidade(item_qnt, item_id)


########################################################################
#                           DELETAR PRODUTO
########################################################################


def deletar_produto(nome):

    nome_item = nome.lower().strip()

    if not nome_item:
        return False, "Nome precisa ser válido"

    resposta, dados = buscar_item_por_nome(nome_item)

    if not resposta:
        return False, dados

    item_id = dados[0]

    return excluir_item(item_id)