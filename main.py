from connection import *

create_connection("postgres", "postgres", "postgres")

query = """
SELECT * from heroes
"""

print(execute_query(query))