import os
import json
import pyodbc
from dotenv import load_dotenv
from DB_operator.DB_operator import ConnectDB
import SQL_Queries


class DBManager:

    def __init__(self, connector_obj):
        self.conn = connector_obj
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_data_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            python_data = json.load(file)
            return python_data

    def fill_table(self, database_name, table_name, filename, sql_query):
        self.cursor.execute(f"USE {database_name}")
        data_to_fill_list = self.get_data_from_json(filename)
        try:
            for data_to_fill in data_to_fill_list:
                self.cursor.execute(sql_query(table_name, data_to_fill))
        except pyodbc.Error as ex:
            return ex
        else:
            return "Данные помещены в таблицу"

        # QUERY = fr"""INSERT INTO {table_name} (employer_id, employer_name, employer_url)
        #                         VALUES
        #                         ('{data_to_fill['id']}',
        #                          '{data_to_fill['name']}',
        #                          '{data_to_fill['alternate_url']}');"""


if __name__ == "__main__":
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    active_db = "EmployersVacancies"

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_manager = DBManager(my_conn)
    print(my_manager.fill_table(active_db, 'Employers', r'data/employers.json', SQL_Queries.fill_employers))
    print(my_manager.fill_table(active_db, 'Vacancies', r'data/vacancies.json', SQL_Queries.fill_vacancies))
