import psycopg

def clent():
    conexio = """
                dbname=postgres
                user=user_postgres
                password=pass_postgres
                host=localhost
                port=5432
            """
    try:
        # Establecer la conexión a la base de datos
        return psycopg.connect(conexio)
    
    except Exception as e:
        print(f"Eroor de coneccion {e}")
