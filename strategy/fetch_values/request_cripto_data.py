import ccxt
import pandas as pd

def request(symbol,timeframe, date, limit):
    exchange = ccxt.binance()
    #al pasar la fecha desde la que queremos recoger los datos debemos pasarlo con el formato completo que es 2020-01-01T00:00:00Z
    since = exchange.parse8601(f'{date}T00:00:00Z')
    
    #pasamos todos los datos a la funcion de ccxt fetch_ohlcv para obtener los datos de apertura, cierre, alto, bajo y volumen y la franja de tiempo
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit)
    columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    data = pd.DataFrame(ohlcv, columns=columns)

    # convertimos los milisegundos de unix en un formato de tipo fecha, para poder analizarlo como datetime
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='ms')
    return data