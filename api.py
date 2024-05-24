import requests

# URL de la API de CoinGecko
url = 'https://api.coingecko.com/api/v3/simple/price'

# Parámetros de la consulta
params = {
    'ids': 'bitcoin',
    'vs_currencies': 'usd'
}

# Hacer la solicitud a la API
response = requests.get(url, params=params)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    bitcoin_price = data['bitcoin']['usd']
    print(f"El precio de Bitcoin es: ${bitcoin_price}")
else:
    print("Error en la solicitud:", response.status_code)