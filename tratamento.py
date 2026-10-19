from pathlib import Path
import pandas as pd

## Informando o caminho do arquivo excel
CAMINHO = Path(r"C:\Users\garci\OneDrive\Desktop\Projeto Exportação\Base_dados\exportacoes_empresa_ficticia.xlsx")

df_bruto = pd.read_excel(CAMINHO, sheet_name="Exportacoes", dtype=str)

##Verificando o tipo das colunas
print(df_bruto.dtypes)

##Vizualizando a quantidade de valores nulos
print(df_bruto.isnull().sum())
coluna = ['Polo', 'Categoria', 'Estado_Destino', 'Cidade_Destino', 'Cliente', 'Forma_Pagamento', 'Status', 'Cod_Peca', 'Quantidade']

for c in coluna:
    df_bruto[c] = df_bruto[c].fillna('Não informado')


print(df_bruto.isnull().sum())

##Excluindo duplicidade
print(f'Quantidade de linhas totais: {df_bruto['ID_Pedido'].count()}')

df_bruto = df_bruto.drop_duplicates(subset = 'ID_Pedido')
print(f'Quantidade de linhas após exclusão: {df_bruto['ID_Pedido'].count()}')

##Tratando valores da coluna Data_Exportacao
print("-------------------------")
print("COLUNA DATA_EXPORTACAO")
print("-------------------------")
df_bruto["Data_Exportacao"] = pd.to_datetime(
    df_bruto["Data_Exportacao"],
    format="mixed", ##Lê cada valor em seu próprio formato
    dayfirst=True, ##Diz que o primeiro valor é a data
    errors="coerce", ## O que não da para converter vira nulo
)

df_bruto["Data_Exportacao"].dt.strftime("%d/%m/%Y")


futuras = df_bruto["Data_Exportacao"] > pd.Timestamp.today() ##Verificando datas futuras
print(f'Datas futuras: {futuras.sum()}')

df_bruto['Data_Exportacao'] = df_bruto['Data_Exportacao'].fillna('NaT') ##Inserindo valores para os nulos
nulas = df_bruto["Data_Exportacao"].isna()
print(f'Datas nulas: {nulas.sum()}')

##Tratando a coluna Polo

print("-------------------------")
print("COLUNA POLO")
print("-------------------------")

polo_nao_informado = df_bruto['Polo'].eq('Não informado') #Verificando não informado
print(f'Polos não informados: {polo_nao_informado.sum()}')

#Excluindo polos não informados
antes = len(df_bruto)
sem_polo = df_bruto['Polo'].eq('Não informado')
excluidas = df_bruto[sem_polo]
df_bruto = df_bruto[~sem_polo].copy()
print("Excluindo Polos não informados") ##Informando dados
print(f"Antes: {antes} | Depois: {len(df_bruto)} | Excluídas: {len(excluidas)}")

#Padronizando os valores
print(df_bruto['Polo'].unique()) #Identificando valores unicos
sp = ['S. Paulo', 'SP', 'São Paulo', 'Sao Paulo', ' SP', 'sp', 'POLO SP', 'Polo SP']
rs = ['RS ', 'Porto Alegre', 'RS', 'R. Grande do Sul', 'POLO RS', 'Polo RS', 'Rio Grande do Sul', 'rs']

df_bruto['Polo'] = df_bruto['Polo'].replace(sp, 'SP')
df_bruto['Polo'] = df_bruto['Polo'].replace(rs, 'RS')
print(df_bruto['Polo'].unique()) ##Verificando normalidade

quant_sp = df_bruto['Polo'].eq('SP').sum()
quant_rs = df_bruto['Polo'].eq('RS').sum()
print(f'Quantidade São Paulo: {quant_sp}')
print(f'Quantidade Rio Grande do Sul: {quant_rs}')

##Tratando a coluna Cod_Peca
print("-------------------------")
print("COLUNA COD_PECA")
print("-------------------------")

df_bruto['Cod_Peca'] = df_bruto['Cod_Peca'].str.upper() ##Deixando a coluna para o P estar em maiúsculo
nao_informado = df_bruto['Cod_Peca'].eq('NÃO INFORMADO')## Verificando valores não informado
informado = df_bruto['Cod_Peca'].str.fullmatch('P\d{3}') ##Verificando valores com P e 3 dígitos depois do P
fora_padrao = (~nao_informado & ~informado) ##Verificando valores que estão fora desse padrão
print(f'Quantidades não informadas: {nao_informado.sum()}')
print(f'Quantidade informada: {informado.sum()}')
print(f'Fora do padrao antes: {fora_padrao.sum()}')
# Identificando os valores fora do padrao

df_bruto['Cod_Peca'] = df_bruto['Cod_Peca'].replace('-', 'NÃO INFORMADO')
nao_informado = df_bruto['Cod_Peca'].eq('NÃO INFORMADO')
informado = df_bruto['Cod_Peca'].str.fullmatch('P\d{3}')
fora_padrao = (~nao_informado & ~informado)
print(f'Fora do padrao agora: {fora_padrao.sum()}')


##Tratando a coluna Cod_Peca
print("-------------------------")
print("COLUNA PECA")
print("-------------------------")

#Verificando quantidade de valores não informados
nao_informado = df_bruto['Peca'].eq('Não informado').sum()
informado = df_bruto['Peca']
print(f'Quantidade Cod_Peca não informados: {nao_informado}')
print(f'Quantidade informada: {informado.count()}')

codigos = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010'] ## Armazenando os códigos
print(df_bruto[['Cod_Peca', 'Peca']].drop_duplicates().sort_values('Cod_Peca')) ##Vizualizando os nomes únicos e seus Códigos

##Após vizualizar e organizar o código abaixo sobreo  código da peça e o nome da peça, foi escrito os valores nulos
## Da coluna cod_peca fazendo engenharia reversa pelo nome da coluna Peca
nome_para_cod = { 
    'rolamento 6204': 'P003',
    'porca autotravante m10': 'P002',
    'valvula pneumática 1/2': 'P006',
    'parafuso sextavado m8': 'P001',
    'flange de aço carbono': 'P008',
}

sem_cod = df_bruto['Cod_Peca'].eq('NÃO INFORMADO') ##Filtro de não informado
chave = df_bruto.loc[sem_cod, 'Peca'].str.strip().str.lower()

df_bruto.loc[sem_cod, 'Cod_Peca'] = chave.map(nome_para_cod).fillna('NÃO INFORMADO')

nomes = { ##Definindo os nomes para cada código padronizando
    'P001': 'Parafuso Sextavado M8',
    'P002': 'Porca Autotravante M10',
    'P003': 'Rolamento Rigido 6204',
    'P004': 'Engrenagem Conica 24D',
    'P005': 'Eixo Transmissão 500mm',
    'P006': 'Válvula Pneumática 1/2',
    'P007': 'Mangueira Hidráulica 3/8',
    'P008': 'Flange de Aço Carbono',
    'P009': 'Correia Dentada HTD 5M',
    'P010': 'Junta de Vedação Viton',
}

df_bruto['Peca'] = df_bruto['Cod_Peca'].map(nomes)
print(df_bruto[['Cod_Peca', 'Peca']].drop_duplicates().sort_values('Cod_Peca'))

print(f'Quantidade Cod_Peca não informados: {nao_informado}')
print(f'Quantidade informada: {informado.count()}')



##Tratando a coluna Categoria
print("-------------------------")
print("COLUNA CATEGORIA")
print("-------------------------")
#Verificando quantidade de não informado e informado
nao_informado = df_bruto['Categoria'].eq('Não informado').sum()
informado = df_bruto['Categoria'].ne('Não informado').sum()
print(f'Categorias não informadas: {nao_informado}')
print(f'Categoria informada: {informado}')

categoria_unica = df_bruto['Categoria'].unique()
print(categoria_unica)

df_bruto['Categoria'] = df_bruto['Categoria'].str.capitalize() ##Padronizando para todos estarem apenas com a primeira letra em maiúsculo
modificar = ['N/d', '-'] ##Armazenando diferanças
df_bruto['Categoria'] = df_bruto['Categoria'].replace(modificar, 'Não informado')
categoria_unica = df_bruto['Categoria'].unique()
print(categoria_unica)

nao_informado = df_bruto['Categoria'].eq('Não informado').sum()
informado = df_bruto['Categoria'].ne('Não informado').sum()
print(f'Categorias não informadas: {nao_informado}')
print(f'Categoria informada: {informado}')

##Verificando a padronização dos códigos e onde os não informados estão
cod_categoria = df_bruto[['Cod_Peca', 'Categoria']].drop_duplicates().sort_values('Cod_Peca') 
print(cod_categoria)

padrao_categoria = {
    'P001': 'Fixadores',
    'P002': 'Fixadores',
    'P003': 'Rolamentos',
    'P004': 'Transmissão',
    'P005': 'Transmissão',
    'P006': 'Pneumática',
    'P007': 'Hidráulica',
    'P008': 'Conexões',
    'P009': 'Transmissão',
    'P010': 'Vedação',
}

df_bruto['Categoria'] = df_bruto['Cod_Peca'].map(padrao_categoria).fillna('Não informado')
cod_categoria_padrao = df_bruto[['Cod_Peca', 'Categoria']].drop_duplicates().sort_values('Cod_Peca') ##Verificando se está padronizado
print(cod_categoria_padrao)

nao_informado = df_bruto['Categoria'].eq('Não informado').sum()
informado = df_bruto['Categoria'].ne('Não informado').sum()
print(f'Categorias não informadas: {nao_informado}')
print(f'Categoria informada: {informado}')



##Tratando a coluna Estado_Destino
print("-------------------------")
print("COLUNA ESTADO DESTINO")
print("-------------------------")
##Verificando os dados unicos
df_bruto['Estado_Destino'] = df_bruto['Estado_Destino'].str.upper().str.strip()
estado_unico = df_bruto['Estado_Destino'].unique()
print(estado_unico)

##Estados
estados = {
    'SP': ['S.P.', 'SÃO PAULO', 'SAO PAULO'],
    'RS': ['RIO GRANDE DO SUL', 'R.S.'],
    'MG': ['MINAS GERAIS', 'MINAS'],
    'GO': ['GOIÁS'],
    'BA': ['BAHIA'],
    'RJ': ['RIO DE JANEIRO', 'R.J.'],
    'PR': ['PARANÁ'],
    'PE': ['PERNAMBUCO'],
    'CE': ['CEARÁ'],
    'SC': ['SANTA CATARINA'],
    'N/D': ['NÃO INFORMADO']
}

##Transcrevendo
for sigla, variacoes in estados.items():
    df_bruto['Estado_Destino'] = df_bruto['Estado_Destino'].replace(variacoes, sigla)

estado_unico = df_bruto['Estado_Destino'].unique()
print(estado_unico)


##Tratando a coluna Cidade_Destino
print("-------------------------")
print("COLUNA CIDADE DESTINO")
print("-------------------------")

df_bruto['Cidade_Destino'] = df_bruto['Cidade_Destino'].str.title().str.strip()
print(df_bruto['Cidade_Destino'].unique()) ##Verificando cidades

cidades = {
    'São José dos Campos': ['São José Dos Campos', 'São José Dos Campo'],
    'Caxias do Sul': ['Caxias Do Sul', 'Caxias Do Su'],
    'Anápolis': ['Anapolis'],
    'Vitória da Conquista': ['Vitória Da Conquista', 'Vitoria Da Conquista'],
    'Londrina': ['Londrin'],
    'Feira de Santana': ['Feira De Santana'],
    'Ribeirão Preto': ['Ribeirao Preto', 'Ribeirão Pret'],
    'Cascavel': ['Cascave'],
    'Juiz de Fora': ['Juiz De Fora'],
    'Campinas': ['Campina'],
    'Rio Verde': ['Rio Verd'],
    'São Paulo': ['Sao Paulo'],
    'Campos dos Goytacazes': ['Campos Dos Goytacazes', 'Campos Dos Goytacaze'],
    'Florianópolis': ['Florianopolis'],
    'Rio de Janeiro': ['Rio De Janeiro'],
    'Curitiba': ['Curitib'],
    'Chapecó': ['Chapec'],
    'Uberlândia': ['Uberlandia'],
    'Blumenau': ['Blumena'],
    'Juazeiro do Norte': ['Juazeiro Do Norte'],
    'Sorocaba': ['Sorocab'],
    'Não informado': ['Não Informado', '-', 'N/D', 'N/A'],
}

for correto, variacoes in cidades.items():
    df_bruto['Cidade_Destino'] = df_bruto['Cidade_Destino'].replace(variacoes, correto)

print(df_bruto['Cidade_Destino'].unique())



##Tratando a coluna Quantidade
print("-------------------------")
print("COLUNA QUANTIDADE")
print("-------------------------")

quantidade = df_bruto['Quantidade'].ne('Não informado')
nao_informado = df_bruto['Quantidade'].eq('Não informado')

print(f'Quantidade informada: {quantidade.sum()}')
print(f'Quantidade não informada: {nao_informado.sum()}')

##Verificando dados unicos
print(df_bruto['Quantidade'].unique())

quantidades = {
    '5': ['5 ', '5 un', '5 UN.'],
    '10': ['dez', '10 un', '10 UN.'],
    '20': ['20 un', '20 UN.'],
    '30': ['30 un', '30 UN.'],
    '50': ['50 un', '50 UN.'],
    '100': ['cem', '100 ', '100 un', '100 UN.'],
    '150': ['150 un', '150 UN.'],
    '200': ['duzentos', '200 un', '200 UN.'],
    '250': ['250 un', '250 UN.'],
    '500': ['500 un', '500 UN.'],
    '1000': ['1.000', '1000 un', '1000 UN.'],
    '1500': ['1.500', '1500 un', '1500 UN.'],
    'NaN': ['-', 'Não informado'],
}

for correto, variacoes in quantidades.items():
    df_bruto['Quantidade'] = df_bruto['Quantidade'].replace(variacoes, correto)

print(df_bruto['Quantidade'].unique())

#Transformando a coluna em numérica
df_bruto['Quantidade'] = pd.to_numeric(df_bruto['Quantidade'], errors='coerce')

nao_informado = df_bruto['Quantidade'].eq('NaN').sum()
incorretas = (df_bruto['Quantidade'] <= 0).sum()# negativas e zero
print(f'Não informadas: {nao_informado} | Incorretas (<= 0): {incorretas}')

##Criando uma nova coluna informando quantidade incorreta ou não informada

df_bruto['Quantidade_Status'] = 'Informado' ##Criando a coluna

df_bruto.loc[df_bruto['Quantidade'].isna(), 'Quantidade_Status'] = 'Não informado' ##Informando os valores não informados

df_bruto.loc[df_bruto['Quantidade'] <= 0, 'Quantidade_Status'] = 'Incorreto' ##Informando os valores incorretos (Os negativos)



##Tratando a coluna Quantidade
print("-------------------------")
print("COLUNA VALOR UNITARIO")
print("-------------------------")

unico = df_bruto['Valor_Unitario']
print(f'Valores não padronizados: {unico.count()}')

def limpar_valor(txt): ##definindo uma função
    if pd.isna(txt): ##Caso o dataframe for null, retorna null
        return 'NaN'
    t = txt.replace('R$', '').strip() ##Tira o cifrão
    if ',' in t:
        t = t.replace('.', '').replace(',', '.') ##Troca virgula por ponto
    return t

df_bruto['Valor_Unitario'] = pd.to_numeric(df_bruto['Valor_Unitario'].apply(limpar_valor), errors='coerce')

unico = df_bruto['Valor_Unitario'].unique()
padrao = df_bruto['Valor_Unitario']
nulos = df_bruto['Valor_Unitario'].isna()
print(f'Valores padronizados: {padrao.count()}')
print(f'Valores nulos: {nulos.sum()}')

print(sorted(df_bruto['Valor_Unitario'].dropna().unique().tolist())) ## Vizuaizando os valores únicos e usando tolist para deixar em decimal

print(df_bruto['Valor_Unitario'].nlargest(5))## Os 5 maiores
print((df_bruto['Valor_Unitario'] == 0).sum())## Quantos zeros
print((df_bruto['Valor_Unitario'] > 1000).sum())## Quantos acima do limite

##Criando coluna auxiliar
df_bruto['Valor_Unitario_Status'] = 'Informado'
df_bruto.loc[df_bruto['Valor_Unitario'].isna(), 'Valor_Unitario_Status'] = 'Não informado'
df_bruto.loc[df_bruto['Valor_Unitario'] >= 1000, 'Valor_Unitario_Status'] = 'Incorreto'
df_bruto.loc[df_bruto['Valor_Unitario'] == 0.0, 'Valor_Unitario_Status'] = 'Incorreto'

padrao = df_bruto['Valor_Unitario']
nulos = df_bruto['Valor_Unitario'].isna()


##Tratando a coluna Custo_Frete
print("-------------------------")
print("COLUNA CUSTO FRETE")
print("-------------------------")

nulos = df_bruto['Custo_Frete'].isna().sum()
unicos = df_bruto['Custo_Frete'].unique()
print(f'Quantidade de custo frete nulos antes: {nulos}')


df_bruto['Custo_Frete'] = pd.to_numeric(df_bruto['Custo_Frete'].apply(limpar_valor), errors='coerce')

unicos = df_bruto['Custo_Frete'].unique()
nulos = df_bruto['Custo_Frete'].isna().sum()
print(f'Quantidade de custo frete nulos depois: {nulos}')

##Criando coluna auxiliar
df_bruto['Custo_Frete_Status'] = 'Informado'
df_bruto.loc[df_bruto['Custo_Frete'].isna(), 'Custo_Frete_Status'] = 'Não informado'
df_bruto.loc[df_bruto['Custo_Frete'] >= 4000, 'Custo_Frete_Status'] = 'Incorreto'
df_bruto.loc[df_bruto['Custo_Frete'] == 0.0, 'Custo_Frete_Status'] = 'Incorreto'


##Tratando a coluna Cliente
print("-------------------------")
print("COLUNA CLIENTE")
print("-------------------------")
unicos = df_bruto['Cliente'].unique()
print(f'Quantidade de nomes sem padrão: {len(unicos)}')

nao_informados = ['N/D', '-']
df_bruto['Cliente'] = df_bruto['Cliente'].replace(nao_informados, 'Não informado')
df_bruto['Cliente'] = df_bruto['Cliente'].str.title().str.rstrip()
unicos = df_bruto['Cliente'].unique()
print(f'Quantidade de nomes padronizados: {len(unicos)}')


##Tratando a coluna Forma_Pagamento
print("-------------------------")
print("COLUNA FORMA DE PAGAMENTO")
print("-------------------------")

unicos = df_bruto['Forma_Pagamento'].unique()
print(f'Quantidade de formas de pagamento sem padrão: {len(unicos)}')

df_bruto['Forma_Pagamento'] = df_bruto['Forma_Pagamento'].str.capitalize().str.rstrip()

incorreto = ['N/d', '-', 'Não Informado']

df_bruto['Forma_Pagamento'] = df_bruto['Forma_Pagamento'].replace(incorreto, 'Não informado')
unicos = df_bruto['Forma_Pagamento'].unique()
print(f'Quantidade de formas de pagamento padronizados: {len(unicos)}')


##Tratando a coluna Status
print("-------------------------")
print("COLUNA STATUS")
print("-------------------------")

unicos = df_bruto['Status'].unique()
print(f'Quantidade de status sem padrão: {len(unicos)}')

df_bruto['Status'] = df_bruto['Status'].str.capitalize().str.rstrip()

incorreto = ['-']
df_bruto['Status'] = df_bruto['Status'].replace(incorreto, 'Não informado')

unicos = df_bruto['Status'].unique()
print(f'Quantidade de formas de pagamento padronizados: {len(unicos)}')


