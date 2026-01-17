import pandas as pd
from sqlalchemy import create_engine
from tqdm.notebook import tqdm
import click

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]
@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2021, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
def ingest_data(user, password, host, port, db, year, month, table):

    # prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    # url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'
    # prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data/'
    # url = f'{prefix}green_tripdata_{year}-{month:02d}.parquet'

    url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # df = pd.read_parquet(url)
    # df.to_sql(
    #     table,  # Name of the table in PostgreSQL
    #     con=engine,  # The SQLAlchemy engine
    #     if_exists='replace',  # 'fail', 'replace', or 'append' if table exists
    #     index=False  # Don't write the DataFrame index as a column
    # )
    df_iter = pd.read_csv(
        url,
        # dtype=dtype,
        # parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )


    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(n=0).to_sql(name=table, con=engine, if_exists='replace')
            first = False
            print("Table created")
        df_chunk.to_sql(name=table, con=engine, if_exists='append')
        print("Inserted:", len(df_chunk))

if __name__ == '__main__':
    ingest_data()

