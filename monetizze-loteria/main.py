from loteria import Loteria

# Criando objeto Loteria
loteria = Loteria(8, 10)

# Gerando os jogos
print(loteria.gera_todos_jogos())

# Gerando as dezenas do sorteio
print(loteria.realiza_sorteio())

# Visualizando o resultado dos jogos na tabela html
print(loteria.visualiza_resultado())
