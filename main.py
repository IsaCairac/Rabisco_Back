import os
import mysql.connector

# Função para limpar a tela
def imprimir_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("- " * 16)
    print("|  *** SISTEMA PAPELARIA ***  |")
    print("- " * 16)

# Estabelecendo conexão com o banco de dados
conexaoDB  = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
    database="Papelaria"
)

# Função para cadastrar um produto
def cadastrar():
    imprimir_header()
    print("----CADASTRO DE PRODUTO----")
    nome = input("Informe o nome do produto: ")
    descricao = input("Digite a descricao: ")
    try:
        preco = float(input("Preco: "))
        quantidade = int(input("Quantidade: "))
    except ValueError:
        print("Erro! Preço e quantidade devem ser valores numéricos")
        return
    if not nome or not descricao or preco <= 0 or quantidade < 0:
        print("Erro! Todos os campos devem ser preenchidos e valores válidos.")
        return
    if len(nome) > 50:
        print("Erro! O nome do produto não pode ter mais de 50 caracteres.")
        return

    comandoSQL = f'INSERT INTO Produto VALUES (null, "{nome}", "{descricao}", {preco}, {quantidade})'

    try:
        cursorDB = conexaoDB.cursor()
        cursorDB.execute(comandoSQL)
        conexaoDB.commit()
    except mysql.connector.Error as erro:
        print(f"Falha ao cadastrar: {erro}")
        return
    print("*** Cadastro realizado com sucesso!")
    cursorDB.close()

# Função para listar todos os produtos cadastrados
def listar_produtos():
    imprimir_header()
    print("---- PRODUTOS CADASTRADOS ----")
    try:
        cursorDB = conexaoDB.cursor()
        cursorDB.execute('SELECT * FROM Produto')
        produtos = cursorDB.fetchall()

        if not produtos:
            print("Não há produtos cadastrados!")
        else:
            for produto in produtos:
                print(f"Id:{produto[0]} | Nome: {produto[1]} | DESCRICAO: {produto[2]} | PRECO: {produto[3]} | QUANT: {produto[4]}")
                print("- " * 50)
    except mysql.connector.Error as erro:
        print(f"Falha ao listar produtos: {erro}")
        return

# Função para excluir um produto pelo ID
def excluir():
    imprimir_header()
    print("*** EXCLUIR PRODUTO ***")
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]}")

    confirma = input("Digite S para confirmar a exclusão: ").upper()
    if confirma != "S":
        print("Exclusão Cancelada!")
        return
    
    try:
        cursorDB = conexaoDB.cursor()
        cursorDB.execute('DELETE FROM Produto WHERE idProduto = %s', (id_produto,))
        conexaoDB.commit()
        print("Produto excluído com sucesso!")
        cursorDB.close()
    except mysql.connector.Error as erro:
        print(f"Falha ao excluir produto: {erro}")

# Função para buscar um produto pelo ID
def get_produto(id_produto):
    try:
        cursorDB = conexaoDB.cursor()
        comandoSQL = f'SELECT * FROM Produto WHERE idProduto = {id_produto}'
        cursorDB.execute(comandoSQL)
        return cursorDB.fetchone()
    except mysql.connector.Error as erro:
        print(f"Falha ao buscar produto: {erro}")
        return None

# Função para alterar a quantidade de um produto
def altera_quantidade():
    imprimir_header()
    print("*** ALTERAR QUANTIDADE DO PRODUTO ***")
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]} - QUANTIDADE: {produto[4]}")

    try:
        nova_quantidade = int(input("Digite a nova quantidade: "))
    except ValueError:
        print("Erro! A nova quantidade deve ser numérica!")
        return

    if nova_quantidade < 0:
        print("Erro! A nova quantidade deve ser maior ou igual a zero!")
        return
    
    confirma = input("Digite S para confirmar a alteração: ").upper()
    if confirma != "S":
        print("Alteração Cancelada!")
        return
    
    try:
        cursorDB = conexaoDB.cursor()
        cursorDB.execute('UPDATE Produto SET quantidade = %s WHERE idProduto = %s', (nova_quantidade, id_produto))
        cursorDB = conexaoDB.cursor()
        conexaoDB.commit()
        print("Quantidade do produto alterada com sucesso!")
        cursorDB.close()
    except mysql.connector.Error as erro:
        print(f"Falha ao alterar quantidade do produto: {erro}")

# Função para alterar o preço de um produto               
def alterar_preco():
    print("- " * 20)
    print("*** ALTERAR PREÇO ***")
    print("- " * 20)
    try:
        id_produto = int(input("Informe o ID do produto: "))
    except ValueError:
        print("Erro! ID deve ser numérico!")
        return
    produto = get_produto(id_produto)

    if not produto:
        print(f"Produto com o ID {id_produto} não encontrado!")
        return
    
    print("Produto encontrado!")
    print(f"ID: {produto[0]} - NOME: {produto[1]} - PREÇO: {produto[3]}")
    
    novo_preco = float(input("Digite o novo preço: "))
    
    try:
        cursorDB = conexaoDB.cursor()
        comandoSQL = f"UPDATE Produto SET preco = {novo_preco} WHERE idProduto = {id_produto}"
        cursorDB.execute(comandoSQL)
        conexaoDB.commit()
        print(f"Preço do produto {produto[1]} atualizado com sucesso!")
        print(f"Novo Preço: {novo_preco}")
        cursorDB.close()
    except mysql.connector.Error as erro:
        print(f"Falha ao alterar preço: {erro}")

#Menu        
while True:
    imprimir_header()
    print("------ MENU -------")
    print("[1] - Cadastar produto ")
    print("[2] - Alterar quantidade ")
    print("[3] - Alterar preco ")
    print("[4] - Mostrar todos os produtos ")
    print("[5] - Excluir um produto ")
    print("[6] - Sair do sistema ")

    opcao = input("\nInforme a opção desejada: ")
    if opcao == '1':
        print("Você escolheu a opção 1")
        cadastrar()
    elif opcao == '2':
        print("Você escolheu a opção 2")
        altera_quantidade()
    elif opcao == '3':
        print("Você escolheu a opção 3")
        alterar_preco()
    elif opcao == '4':
        print("Você escolheu a opção 4")
        listar_produtos()
    elif opcao == '5':
        print("Você escolheu a opção 5")
        excluir()
    elif opcao == '6':
        break
    else:
        print("Opção inválida!")

    input("Pressione Enter para continuar...")
print("SISTEMA ENCERRADO!")
conexaoDB.close()