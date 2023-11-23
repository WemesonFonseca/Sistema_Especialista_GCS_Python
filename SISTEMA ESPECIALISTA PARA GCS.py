# Biblioteca para usar pausa na execulção do programa
from time import sleep
print('-=' * 5, 'ESCALA DE GLASGOW', '=-' * 5)

print('\033[4mPara as perguntas abaixo responda\033[m \033[32m[Sim]\033[m ou \033[31m[Não]\033[m\n')

# 2 segundos antes de aparecer as perguntas
sleep(2)

# Variáveis para armazenar os resultados
AvaliacaoOcular = 0
AvaliacaoVerbal = 0
AvaliacaoMotora = 0

# Avaliação Ocular
print('1 - Avaliação Ocular\n')
avaliacaoOcular1 = str(input('Os olhos do paciente estão abertos sem nenhum estímulo?: ')).lower()

# Armazenando a resposta da Avaliação Ocular
if avaliacaoOcular1 == 'sim':
    AvaliacaoOcular = 4
else:
    avaliacaoOcular2 = str(input('Após solicitação verbal o paciente abre os olhos?: ')).lower()
    if avaliacaoOcular2 == 'sim':
        AvaliacaoOcular = 3
    else:
        avaliacaoOcular3 = str(input('Se efetuar um estímulo físico o paciente abre os olhos?: ')).lower()
        if avaliacaoOcular3 == 'sim':
            AvaliacaoOcular = 2
        else:
            AvaliacaoOcular = 1

# Avaliação Verbal
print('\n')
print('2 - Avaliação Verbal\n')
avaliacaoVerbal1 = str(input('O paciente responde o nome dele corretamente?: ')).lower()

# Armazenando a resposta da Avaliação Verbal
if avaliacaoVerbal1 == 'sim':
    AvaliacaoVerbal = 5
else:
    avaliacaoVerbal2 = str(input('O paciente responde qual o mês atual corretamente?: ')).lower()
    if avaliacaoVerbal2 == 'sim':
        AvaliacaoVerbal = 4
    else:
        avaliacaoVerbal3 = str(input('O paciente formula uma frase que faz sentido?: ')).lower()
        if avaliacaoVerbal3 == 'sim':
            AvaliacaoVerbal = 3
        else:
            avaliacaoVerbal4 = str(input('O paciente emite sons ou gemidos?: ')).lower()
            if avaliacaoVerbal4 == 'sim':
                rAvaliacaoVerbal = 2
            else:
                AvaliacaoVerbal = 1

# Avaliação Motora
print('\n')
print('3 - Avaliação Motora\n')
avaliacaoMotora1 = str(input('Após apertar o trapézio do paciente com os dedos formando uma pinça, ele levanta o braço\n'
'de forma rápida com um movimento completo e natural em direção ao local de onde está sendo apertado?: ')).lower()

# Armazenando a resposta da Avaliação Motora
if avaliacaoMotora1 == 'sim':
    AvaliacaoMotora = 5
else:
    avaliacaoMotora2 = str(input('O movimento é encurtado, de forma lenta com o braço sempre próximo ao corpo?: ')).lower()
    if avaliacaoMotora2 == 'sim':
        AvaliacaoMotora = 4
    else:
        avaliacaoMotora3 = str(input('O paciente dobra o braço exercendo um movimento fora do comum?: ')).lower()
        if avaliacaoMotora3 == 'sim':
            AvaliacaoMotora = 3
        else:
            avaliacaoMotora4 = str(input('O paciente estende o braço exercendo um movimento fora do comum?: ')).lower()
            if avaliacaoMotora4 == 'sim':
                AvaliacaoMotora = 2
            else:
                AvaliacaoMotora = 1

# Calculando o total
print('\n')
total = AvaliacaoOcular + AvaliacaoVerbal + AvaliacaoMotora
resultado_final = f"Resposta ocular é de grau: {AvaliacaoOcular}\nResposta verbal é de grau: {AvaliacaoVerbal}\nResposta motora é de grau: {AvaliacaoMotora}\nResultado: {total}"
print(resultado_final)

# Classificação
if total < 9:
    print('A classificação da escala de Glasgow é \033[31mGRAVE\033[m')
elif total <= 11:
    print('A classificação da escala de Glasgow é \033[33mMÉDIO\033[m')
else:
    print('A classificação da escala de Glasgow é \033[32mLEVE\033[m')

# Bibliotecas para o banco de dados SQL
import mysql.connector
# Biblioteca para vizualizar os dados em python
import matplotlib.pyplot as plt

# Conexão com o banco de dados local
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="escala_glasgow"
)

mycursor = mydb.cursor()

# Nome do paciente
nome_paciente = str(input('Qual o nome do paciente?: '))

# Salvar avaliação no banco de dados
sql = "INSERT INTO paciente (nome_paciente, Avaliacao_ocular, Avaliacao_verbal, Avaliacao_motora) VALUES (%s, %s, %s, %s)"
val = (nome_paciente, AvaliacaoOcular, AvaliacaoVerbal, AvaliacaoMotora)
mycursor.execute(sql, val)
mydb.commit()

# Função para buscar todos os resultados anteriores de uma avaliação específica para o paciente
def buscar_resultados_anteriores(tipo_avaliacao):
    sql = f"SELECT {tipo_avaliacao} FROM paciente WHERE nome_paciente = %s"
    mycursor.execute(sql, (nome_paciente,))
    resultados = mycursor.fetchall()
    return [resultado[0] for resultado in resultados]

# Resultados anteriores
resultados_labels = ['Avaliacao_ocular', 'Avaliacao_verbal', 'Avaliacao_motora']
ultimos_resultados_anteriores = []
for tipo_avaliacao in resultados_labels:
    ultimos_resultados_anteriores.append(buscar_resultados_anteriores(tipo_avaliacao))

# Resultados atuais
resultados_atuais = [AvaliacaoOcular, AvaliacaoVerbal, AvaliacaoMotora]
fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for i in range(3):

# Criação dos gráficos
    axs[i].plot(range(len(ultimos_resultados_anteriores[i])), ultimos_resultados_anteriores[i], marker='o', linestyle='-', color='blue')
    axs[i].scatter(len(ultimos_resultados_anteriores[i]), resultados_atuais[i], label='Atual', color='red', s=100)
    axs[i].set_xticks(range(len(ultimos_resultados_anteriores[i]) + 1))
    axs[i].set_xticklabels([f'Aval {i}' for i in range(1, len(ultimos_resultados_anteriores[i]) + 1)] + ['Atual'])
    axs[i].set_ylabel('Pontuação')
    axs[i].set_title(resultados_labels[i])
    axs[i].legend()
plt.tight_layout()
plt.show()
