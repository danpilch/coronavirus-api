import os
import pandas as pd
import sqlalchemy
from arcgis.gis import GIS
from pathlib import Path
from zipfile import ZipFile
import datetime


class Data(object):
    def __init__(self):
        self.version = os.getenv('VERSION', None)

        self.api_dataset_id = os.getenv('API_DATASET_ID', 'b684319181f94875a6879bbc833ca3a6')
        self.api_dataset_filename = os.getenv('API_DATASET_FILENAME', 'CountyUAscasestable.csv')
        # comma-separated columns to use
        self.api_dataset_columns = os.getenv('API_DATASET_COLUMNS', 'GSS_NM,TotalCases').split(',')
        self.api_dataset_replace_columns = os.getenv('API_DATASET_REPLACE_COLUMNS', 'county_name,cases').split(',')

        self.db_host = os.getenv('MYSQL_HOST', '127.0.0.1') 
        self.db_user = os.getenv('MYSQL_USER', 'api')
        self.db_pass = os.getenv('MYSQL_PASS', 'api')
        self.db_name = os.getenv('MYSQL_NAME', 'cv')
        self.db_table = os.getenv('MYSQL_TABLE_NAME', 'county_data')

        self.data_path = "/tmp/data"

    def get_data(self):
        try:
            # Auth to arcgis
            anon_gis = GIS()
            # Define dataset id
            data_item = anon_gis.content.get(self.api_dataset_id)
            # Setup data storage path
            data_path = Path(self.data_path)
            if not data_path.exists():
                data_path.mkdir()
            # Download dataset
            data_item.download(save_path=data_path)
            # Just find the first file, as it'll always only be one
            self.data_path_file = list(file for file in data_path.glob('*'))[0]
        except Exception as e:
            raise e

    def insert_data(self):
        try:
            engine = sqlalchemy.create_engine(f'mysql+pymysql://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}')
            pd_df = pd.read_csv(self.data_path_file, usecols=self.api_dataset_columns)
            # Rename columns to frienly names
            pd_df = pd_df.rename(columns=dict(zip(self.api_dataset_columns, self.api_dataset_replace_columns)))
            # Add a timestamp column of datetimenow
            pd_df['timestamp'] = datetime.datetime.now()
            # push dataframe to sql table
            pd_df.to_sql(self.db_table, con=engine, if_exists='replace', index=True, index_label='id')
            print("completed")
        except Exception as e:
            raise e


def main():
    data = Data()
    data.get_data()
    data.insert_data()

if __name__ == "__main__":
    main()
