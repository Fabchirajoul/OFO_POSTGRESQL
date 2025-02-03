import psycopg2

import psycopg2

def get_db_connection():
    try:
        connection = psycopg2.connect(
            "postgresql://randrefinerydb_hdcz_user:NJY9sBdbbw3Sipd0gFGhHFjlLoiWnaaD@dpg-cudl8flumphs73cpbcj0-a.oregon-postgres.render.com/randrefinerydb_hdcz"
        )
        return connection
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
        return None






def initialize_database(sql_file_path):
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return
    
    try:
        cursor = connection.cursor()
        
        # Read the SQL script file
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()
        
        # Execute the SQL script
        cursor.execute(sql_script)
        connection.commit()
        print("Database initialized successfully.")
    except Exception as e:
        print("Error initializing the database:", e)
    finally:
        connection.close()

if __name__ == "__main__":
    # Path to your SQL file
    sql_file_path = 'D:/SHARING PROJECTS/OFO POSTGRESQL/postgrescript.sql'
    initialize_database(sql_file_path)


















# import psycopg2

# def check_tables():
#     try:
#         conn = psycopg2.connect(
#             dbname="randrefinerydb",
#             user="randrefinerydb",
#             password="iFRvbIFDKeSweogzDdaIisdjVGfvStv1",
#             host="dpg-ct2rlqjtq21c73b73sp0-a",
#             port="5432"
#         )
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT table_name
#             FROM information_schema.tables
#             WHERE table_schema = 'public';
#         """)
#         tables = cursor.fetchall()
#         print("Tables in the database:")
#         for table in tables:
#             print(table[0])
#         conn.close()
#     except Exception as e:
#         print("Error:", e)

# check_tables()
