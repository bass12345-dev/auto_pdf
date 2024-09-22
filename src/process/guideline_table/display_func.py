from src.process.query.query import input_query
from src.process.custom.interpret_sql import interpret_headers, interpret_rows

def main_headers(headers):
    try:
        data = input_query(headers)
        interpreted = interpret_headers(data)
        return interpreted
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e), 500

def rows_display(rows):
    try:
        data = input_query(rows)
        interpreted = interpret_rows(data)
        return interpreted
    except Exception as e:
        print(f"An error occurred: {e}")

        return str(e), 500