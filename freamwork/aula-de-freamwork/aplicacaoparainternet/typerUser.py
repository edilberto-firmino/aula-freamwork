#simular um cadastro de tipos de usuarios e 
#if(@suer = tipo 1 ) = mostra conteudo aaquele tipo de usuatio 

user = input("Digite o tipo de usuário (tipo1 ou tipo2 ou tipo3): ");
nome = input("Digite seu nome: ");
data_nascimento = input("Digite sua data de nascimento (dd/mm/aaaa): ");

if user == "tipo1":
    print(f"Bem-vindo {nome}, você é Administrador dessa empresa pode ver tudo.")
    print(f"{nome}, aqui voce pdoerá ver, contas de banco, RH, Demitir, contratar etc")
    print(f"Sua data de nascimento é: {data_nascimento}")
    
if user == "tipo2":
    print(f"Bem-vindo {nome}, você programdor dessa empresa só pode ver codigo.")
    print(f"{nome}, aqui voce pdoerá ver o código da empresa")
    print(f"Sua data de nascimento é: {data_nascimento}")
if user == "tipo3":
    print(f"Bem-vindo {nome}, você é um usuário comum dessa empresa só pode ver o que a empresa disponibiliza.")
    print(f"{nome}, aqui você poderá ver as informações disponíveis para usuários comuns.")
    print(f"Sua data de nascimento é: {data_nascimento}")