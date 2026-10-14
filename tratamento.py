from pathlib import Path
import pandas as pd

## Informando o caminho do arquivo excel
CAMINHO = Path(r"C:\Users\garci\OneDrive\Desktop\Projeto Exportação\Base_dados\exportacoes_empresa_ficticia.xlsx")

df_bruto = pd.read_excel(CAMINHO, sheet_name="Exportacoes", dtype=str)

##Verificando o tipo das colunas
#print(df_bruto.dtypes)

##Vizualizando a quantidade de valores nulos
#print(df_bruto.isnull().sum())
coluna = ['Polo', 'Categoria', 'Estado_Destino', 'Cidade_Destino', 'Cliente', 'Forma_Pagamento', 'Status', 'Cod_Peca', 'Data_Exportacao']

for c in coluna:
    df_bruto[c] = df_bruto[c].fillna('Não informado')


print(df_bruto.isnull().sum())

##Excluindo duplicidade
df_bruto = df_bruto.drop_duplicates()
print(df_bruto.duplicated().sum())




##Tratando a coluna Cod_Peca

df_bruto['Cod_Peca'] = df_bruto['Cod_Peca'].str.upper()



diferente = []

nao_informado = df_bruto['Cod_Peca'].eq('NÃO INFORMADO')
informado = df_bruto['Cod_Peca'].str.fullmatch('P\d{3}')

print(f'Quantidades não informadas: {nao_informado.sum()}')
print(f'Quantidade informada: {informado.sum()}')


## Identificando os valores fora do padrao

df_bruto['Cod_Peca'] = df_bruto['Cod_Peca'].replace('-', 'NÃO INFORMADO')
nao_informado = df_bruto['Cod_Peca'].eq('NÃO INFORMADO')
informado = df_bruto['Cod_Peca'].str.fullmatch('P\d{3}')
fora_padrao = (~nao_informado & ~informado)

suspeitos = df_bruto.loc[df_bruto["Cod_Peca"].str.contains("-", na=False), "Cod_Peca"]
print(suspeitos.map(repr)) ##Confirmando se o '-' está na lista






##Tratando valores da coluna Data_Exportacao



print("-------------------------")
#Tratando valores da coluna Valor_Unitario
nulos = df_bruto[df_bruto['Valor_Unitario'].isna()] #Buscando apenas as linhas nulas

##Armazenando o nome das peças com valores unitários nulos
pecas = []
#for i in nulos['Peca']:
#    pecas.append(i)
#print(pecas)


#valores = df_bruto.groupby('Peca')['Valor_Unitario']

#print(df_bruto.isnull().sum())


