# Decisões

### Decisão 1:
Os dados brutos estão intocados, a planilha original apenas é lida e os resultados são gerados em outro arquivo.

Leitura do pandas utilizando (dtype= str) para o tipo das colunas serem um padrão, com a conversão ficando sob meu controle.

Duplicatadas removidas com critério sendo da coluna ID_Pedido apenas, com o valor de linhas de 332 para 320, contendo 12 duplicidades.

As colunas de Texto recebem o valor "Não informado" nos ausentes.

Colunas numéricas e de data (Quantidade, Valor_Unitario, Data_Exportacao) ficam nulas, o "Não informado" aparece apenas no Power BI por meio de colunas de Status. Isso evita que os textos quebrem os cálculos

Colunas adicionais (Quantidade_Status, Valor_Status) foram criadas, usadas de suporte para as colunas Quantidade e Valor_Unitario, conténdo linhas como Informado, Não informado ou Incorreto que alimentam o relatório de qualidade e rodapé do dashboard.

Valor unitário não foi preenchido com cálculo. Mediana ou média seriam especulações sobre um dado que é um fato registrado, então o nulo permanece e a linha fica sem receita calculável, mantendo uma precisão maior dos relatórios.

Datas foram convertidas com pd.to_datetime, fazendo o tipo da coluna ser de data e não texto.

Polo padronizado com replace e listas de variações, método escolhido por ser simples de entender e manter. Porto alegre na coluna de polo foi tratado como RS.

Linhas sem polo foram excluídas, pois sem a origem não há como calcular a distância. A quantidade excluída será informada.

Recuperação por engenharia reversa. Códigos ausentes recuperados pelo nome da peça e categorias ausentes pelo código usando a coluna Cod_Peca como referência.

Estado e cidade padronizados com dicionários de variações. A cidade passou antes por .str.title().str.strip(), e as preposições (do, dos, de) foram corrigidas no dicionário.

Quantidade padronizada com dicionário. Textos como 50 un e dez viram número, e - e não informados viram nulos, tendo a coluna Quantidade_Status como auxiliar.

Valor unitário convertido de texto para número com uma regra simples: se há vírgula, os pontos são milhares e a vírgula é o decimal. Se não há, o ponto já é o decimal.

Premissas do negócio e dos dados
Empresa e dados fictícios, gerados para praticar limpeza e análise.

Dois polos existentes: São Paulo (SP) e Rio Grande do Sul (RS). As cidades-sede (São Paulo e Porto Alegre) são premissas.
Distâncias aproximadas, em km rodoviários, feitas sem mapa em tempo real e que devem ser validadas.

Entrega dentro da cidade do polo fixada em 20 km.
Combustível: gasolina a R$ 6,60/litro (média nacional ANP de 24/07/2026) e consumo de 8 km/L, ambos premissas editáveis.

Preço único para todos os estados, uma simplificação, e o custo considera só combustível (sem pedágio, motorista ou custo de construir o polo).

A receita (Quantidade × Valor_Unitario) só é calculada quando os dois valores estão corretos, então o total por estado é um pouco subestimado.



Ainda em aberto, decida e registre
Quantidades <= 0 (-50, -10, 0): Elas contam como incorretas, não vão ser utilizadas em cálculos.

Preços incorretos (zero e acima do limite escolhido, como R$ 1.000): continuam na coluna ou viram nulos, depois de marcar o status? E qual limite você adotou?
Frete: como tratar zeros, absurdos e ausentes.
Datas inválidas e no futuro (31/02/2025 e 2027): como tratar.
Estados ausentes (N/D): recuperar pela cidade ou deixar como não informado.
Pedidos cancelados entram na demanda?
Grafia do “não informado”: hoje há NÃO INFORMADO em umas colunas e Não informado em outras. Escolha uma.
Ida ou ida e volta no cálculo da distância.