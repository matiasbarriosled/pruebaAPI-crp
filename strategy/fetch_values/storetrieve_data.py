import pandas as pd
import fetch_values.request_cripto_data as rcripto
import mysql.connector
from mysql.connector import Error

#borra la tabla completa pasada en el argumento
def drop_table_if_exist(table_name):
    try:
        conn = mysql.connector.connect(
                host='localhost',
                database='backtesting',
                user='pruebas',
                password='contraseñaprueba'
            )
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

    except Error as e:
        print(f'Error: {e}')
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a MySQL cerrada.")


def new_data(symbol, timeframe, date, limit):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='backtesting',
            user='pruebas',
            password='contraseñaprueba'
        )
        if conn.is_connected():
            data = rcripto.request(symbol,timeframe, date, limit)

            cursor = conn.cursor()
            #punto importante a mencionar, el replace es utilizado aca para reemplazar el '/' por el '_' debido a que en MySQL no acepta el caracter '/' en el nombre de las tablas
            #lower para que quede el nombre de tabla en minuscula
            symbol_sql = symbol.replace('/', '_').lower()
            cursor.execute(f'''
               CREATE TABLE IF NOT EXISTS {symbol_sql}_{timeframe}(
                    Timestamp DATETIME,
                    Open DOUBLE,
                    High DOUBLE,
                    Low Double,
                    Close DOUBLE,
                    Volume DOUBLE,
                    PRIMARY KEY (Timestamp)
               )
            ''')
            #el ON DUPLICATE KEY UPDATE me sirve para que en caso de que se carguen datos que ya existan con el mismo horario o fecha
            #no se graben en las tablas, evitando duplicados
            for row in data.itertuples(index=False):
                cursor.execute(f'''
                    INSERT INTO {symbol_sql}_{timeframe}(Timestamp,Open,High,Low,Close,Volume)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    Open=VALUES(Open),
                    High=VALUES(High),
                    Low=VALUES(Low),
                    Close=VALUES(Close),
                    Volume=VALUES(Volume)
                ''', (
                row.Timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                row.Open,
                row.High,
                row.Low,
                row.Close,
                row.Volume
            ))
        conn.commit()
        print("Datos almacenados!")

    except Error as e:
        print(f'Error: {e}')
    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión a MySQL cerrada.")


def fetch_data(symbol, timeframe, date, limit):
    conn = None
    try:
        # Conéctate a la base de datos MySQL
        conn = mysql.connector.connect(
            host='localhost',
            database='backtesting',
            user='pruebas',
            password='contraseñaprueba'
        )
        symbol_sql = symbol.replace('/', '_').lower()
        if conn.is_connected():
            # Ejecuta la consulta para obtener los datos
            query = f"SELECT * FROM {symbol_sql}_{timeframe} WHERE Timestamp>{date} ORDER BY Timestamp LIMIT {limit}"
            df = pd.read_sql(query, conn)

            print("Datos obtenidos de la base de datos:")
            return df

    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Conexión a MySQL cerrada.")
