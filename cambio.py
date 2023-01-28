import requests, json
from datetime import datetime
import yfinance as yf
import os

def update_currency(currency):
    # Load current date and time
    current_date = datetime.now().date()
    current_time = str(datetime.now())
    file_name = f"database/{currency}_quote.json"

    # Check if file exists
    if not os.path.exists(file_name):
        print(f"Error: {file_name} does not exist.")
        model_json = '[{"cotacaoCompra": 0.0, "cotacaoVenda": 0.0, "dataHoraCotacao": "2023-01-01 13:00:00.000", "tipoBoletim": "Fechamento"}]'

        # Save updated file
        with open(file_name, "w") as outfile:
            outfile.write(model_json)
        print("model json quote")

    # Load database
    with open(file_name, "r") as json_file:
        quotes = json.load(json_file)

    # Iterate through quotes
    for quote in quotes:
        quote_datetime = quote["dataHoraCotacao"]
        bulletin_type = quote["tipoBoletim"]

        # Filter values from string
        quote_date, quote_time = quote_datetime.split(" ")
        current_time = current_time.split(" ")[1].split(":")
        quote_time = quote_time.split(":")
        weekend = datetime.now().weekday()

        # Calculate time difference
        hour_diff = int(current_time[0]) - int(quote_time[0])
        minute_diff = int(current_time[1]) - int(quote_time[1])

    # Check if data is up to date
    if str(current_date) == quote_date and bulletin_type == "Fechamento":
        print("Data is up to date, no need to request again")
        return

    if weekend <= 4:
        # Format date for API
        formatted_date = f"{current_date.month}-{current_date.day}-{current_date.year}"
        currency = currency.upper()

        # Request data from API
        endpoint = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaAberturaOuIntermediario(codigoMoeda=@codigoMoeda,dataCotacao=@dataCotacao)?@codigoMoeda='{}'&@dataCotacao='{}'&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao,tipoBoletim"
        endpoint = endpoint.format(currency, formatted_date)
        requested_quote = requests.get(endpoint).json()['value']

        if str(requested_quote) != "[]":
            # Save updated file
            with open(file_name, "w") as outfile:
                json.dump(requested_quote, outfile)
                print("Data successfully updated")
        
        else:
            print("error data")
    
    else:
        print("Close market")

update_currency('usd')

def update_stocks(stock):
    stock_data = yf.download(stock, start='2023-01-26', end='2023-01-27')