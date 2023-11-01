from psycopg2 import connect, OperationalError

def create_connection(db_name, db_user, db_password, db_host = "localhost", db_port = "5432"):
    connection = None
    try:
        connection = connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        print("Query executed successfully")
        return cursor.fetchall()
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")
        return []
    finally:
        connection.close()

def execute_modify(query, params=None):
    connection = create_connection("postgres", "postgres", "postgres")
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        print("Query executed successfully")
    except OSError as e:
        print(f"The error '{e}' occurred or the hero name is already taken")
    finally:
        connection.close()
        