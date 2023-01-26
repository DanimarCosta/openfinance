import requests, json
from datetime import datetime

def atualizar(moeda):
    # Carrega a data do sistema
    data_atual = datetime.now().date()
    name_file = "cotacao_" + moeda + ".json"

    # Carrega o banco de dados
    with open(name_file, "r") as json_usd:
        cotacoes = json.load(json_usd)
        #print(cotacoes)

    for x in cotacoes:
        dataHoraCotacao = x["dataHoraCotacao"]

        # Filtra os valores da string
        data_cotacao = dataHoraCotacao.split(" ")
        data_cotacao = str(data_cotacao[0])
        data_atual = str(data_atual)

    # Verifica se os dados estão atualizados
    if data_atual == data_cotacao:
        print("Não é necessario requisitar os dados, banco de dados atualizado")
        pass

    else:
        # Converte as datas no formato do banco de dados
        data_atual = str(data_atual)
        dia_mes_ano = data_atual.split("-")
        formato_mes_dia_ano = dia_mes_ano[1] + "-" + dia_mes_ano[2] + "-" + dia_mes_ano [0]
        cambio = str(moeda).upper()

        # Realiza a requisição dos dados na API
        endpoint = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodoFechamento(codigoMoeda=@codigoMoeda,dataInicialCotacao=@dataInicialCotacao,dataFinalCotacao=@dataFinalCotacao)?@codigoMoeda='{}'&@dataInicialCotacao='{}'&@dataFinalCotacao='{}'&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
        endpoint = endpoint.format(cambio, formato_mes_dia_ano, formato_mes_dia_ano)
        cotacao_requisitada = requests.get(endpoint)
        cotacao_moeda = cotacao_requisitada.json()['value']

        # Salva o arquivo atualizado
        with open(name_file, "w") as outfile:
            json.dump(cotacao_moeda, outfile)
            print("Banco de dados atualizado com sucesso")

atualizar("eur")