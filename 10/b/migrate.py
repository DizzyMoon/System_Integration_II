
import pymysql
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
import re
import os

load_dotenv()

## MySQL config
mysql_host = os.getenv('MYSQL_HOST')
mysql_user = os.getenv('MYSQL_USER')
mysql_password = os.getenv('MYSQL_PASSWORD')
mysql_database = os.getenv('MYSQL_DATABASE')
mysql_port = os.getenv('MYSQL_PORT')

## PostgreSQL config
ps_host = os.getenv('PS_HOST')
ps_user = os.getenv('PS_USER')
ps_password = os.getenv('PS_PASSWORD')
ps_database = os.getenv('PS_DATABASE')
ps_port = os.getenv('PS_PORT')


# MySQL connection settings
mysql_config = {
    "host": mysql_host,
    "user": mysql_user,
    "password": mysql_password,
    "database": mysql_database,
    "port": mysql_port
}

# PostgreSQL connection settings
pg_config = {
    "host": ps_host,
    "user": ps_user,
    "password": ps_password,
    "dbname": ps_database,
    "port": ps_port
}

def mysql_to_postgres_type(mysql_type):
    # Basic type mapping
    type_map = {
        "int": "INTEGER",
        "tinyint": "SMALLINT",
        "smallint": "SMALLINT",
        "mediumint": "INTEGER",
        "bigint": "BIGINT",
        "varchar": "VARCHAR",
        "char": "CHAR",
        "text": "TEXT",
        "mediumtext": "TEXT",
        "longtext": "TEXT",
        "datetime": "TIMESTAMP",
        "timestamp": "TIMESTAMP",
        "date": "DATE",
        "float": "REAL",
        "double": "DOUBLE PRECISION",
        "decimal": "NUMERIC",
        "blob": "BYTEA"
    }
    match = re.match(r"(\w+)", mysql_type)
    if match:
        base_type = match.group(1).lower()
        return type_map.get(base_type, "TEXT")
    return "TEXT"

def migrate_schema(mysql_conn, pg_conn):
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute("SHOW TABLES")
    tables = [row[0] for row in mysql_cursor.fetchall()]

    pg_cursor = pg_conn.cursor()

    for table in tables:
        mysql_cursor.execute(f"SHOW COLUMNS FROM {table}")
        columns = mysql_cursor.fetchall()

        col_defs = []
        for col in columns:
            name = col[0]
            type_ = mysql_to_postgres_type(col[1])
            null = "NOT NULL" if col[2] == "NO" else ""
            col_defs.append(f'"{name}" {type_} {null}')
        
        create_stmt = f'CREATE TABLE "{table}" ({", ".join(col_defs)});'
        print(f"Creating table: {table}")
        pg_cursor.execute(f"DROP TABLE IF EXISTS \"{table}\" CASCADE;")
        pg_cursor.execute(create_stmt)
        pg_conn.commit()

def migrate_data(mysql_conn, pg_conn):
    mysql_cursor = mysql_conn.cursor()
    pg_cursor = pg_conn.cursor()
    mysql_cursor.execute("SHOW TABLES")
    tables = [row[0] for row in mysql_cursor.fetchall()]

    for table in tables:
        mysql_cursor.execute(f"SELECT * FROM {table}")
        rows = mysql_cursor.fetchall()
        if not rows:
            continue

        columns = [desc[0] for desc in mysql_cursor.description]
        col_list = ', '.join(f'"{col}"' for col in columns)
        placeholders = ', '.join(['%s'] * len(columns))

        for row in rows:
            insert_stmt = f'INSERT INTO "{table}" ({col_list}) VALUES ({placeholders});'
            pg_cursor.execute(insert_stmt, row)

        pg_conn.commit()
        print(f"Migrated {len(rows)} rows from {table}")

def main():
    mysql_conn = pymysql.connect(**mysql_config)
    pg_conn = psycopg2.connect(**pg_config)

    try:
        migrate_schema(mysql_conn, pg_conn)
        migrate_data(mysql_conn, pg_conn)
        print("Migration complete.")
    finally:
        mysql_conn.close()
        pg_conn.close()

if __name__ == "__main__":
    main()
