from pathlib import Path
import pandas as pd

## Informando o caminho do arquivo excel
CAMINHO = Path(r"C:\Users\garci\OneDrive\Desktop\Projeto Exportação\Base_dados\exportacoes_empresa_ficticia.xlsx")

df_bruto = pd.read_excel(CAMINHO, sheet_name="Exportacoes", dtype=str)

##Verificando o tipo das colunas
#print(df_bruto.dtypes)

##Vizualizando a quantidade de valores nulos
#print(df_bruto.isnull().sum())
coluna = ['Polo', 'Categoria', 'Estado_Destino', 'Cidade_Destino', 'Cliente', 'Forma_Pagamento', 'Status', 'Cod_Peca']

for c in coluna:
    df_bruto[c] = df_bruto[c].fillna('Não informado')


print(df_bruto.isnull().sum())

##Excluindo duplicidade
df_bruto = df_bruto.drop_duplicates(subset = 'ID_Pedido')


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
print("-------------------------")


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

codigos = ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P0010'] ## Armazenando os códigos
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

