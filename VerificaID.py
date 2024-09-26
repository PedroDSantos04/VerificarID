import pandas as pd

# Pegando as os arquivos que serão utilizas na verificação
df_cont = pd.read_csv("C:/Users/raflo/OneDrive/Área de Trabalho/Controle de envios.csv", on_bad_lines='skip', sep=";")
df_hyst = pd.read_csv("C:/Users/raflo/OneDrive/Área de Trabalho/TRACKING_HYST_2024_09_26.csv", sep=";")

# Removendo todas as empresas que não enviaram o relatório semanal
df_cont = df_cont[~df_cont['Status'].isin(['NÃO RECEBIDO'])]

# Seleciona somente as colunas que serão interessantes nesse momento, apagando todas as que estão vazias
# e transformando o código da empresa em int
df_cont = df_cont[['Cliente', 'COD CLIENTE']]
df_cont = df_cont.dropna(axis=0)
df_cont['COD CLIENTE'] = df_cont['COD CLIENTE'].astype(int)

# Mesma coisa da parte de cima, só que nesse não tem valores em brancos que estçao atrapalhando
df_hyst = df_hyst[['Cod. Cliente', 'Varejo']]
df_hyst['Cod. Cliente'] = df_hyst['Cod. Cliente'].astype(int)

# criando um dicionário pra receber o resultado das buscas
resultados = []

# Nesse bloco será realizado a busca dos códigos dos clientes na planilha HYST e vai verificar se eles estão corretos, comparando
# na planilha controle de envio, que possuí os códigos correto
for _, row in df_hyst.iterrows():
    cod_cliente = row['Cod. Cliente']
    varejo = row['Varejo']

# Aqui é feita a adição dos valores ao dicionário
    if cod_cliente in df_cont['COD CLIENTE'].values:
       if cod_cliente not in df_cont['COD CLIENTE'].values:
        resultados.append({'COD CLIENTE': cod_cliente, 'Varejo': varejo, 'Status': 'Está correto'})
    else:
        resultados.append({'COD CLIENTE': cod_cliente, 'Varejo': varejo, 'Status': 'Não está correto'})

# Transformando o dicionário em DataFrame
df_result = pd.DataFrame(resultados)

# Apresentando apenas os não estão com os códigos corretos
df_result_err = df_result[df_result['Status'] == 'Não está correto']
print(df_result_err)
