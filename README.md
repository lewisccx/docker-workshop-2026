# docker-workshop-2026

"self ref"
data-engineering-zoomcamp-2026

$ docker run -it --rm --entrypoint=bash -v D:/docker-workshop-2026/test:/app/test python:3.13.11-slim
uv run python ingest_data.py  --network=pg-network --pg-user=root   --pg-pass=root   --pg-host=localhost   --pg-port=5432   --pg-db=ny_taxi   --target-table=yellow_taxi_data

docker run -it \
    --network=pg-network \ 
    --name pgdatabase \
    -e POSTGRES_USER="root" \   
    -e POSTGRES_PASSWORD="root" \  
    -e POSTGRES_DB="ny_taxi" \ 
    -v ny_taxi_postgres_data:/var/lib/postgresql \  
    -p 5432:5432 \  
    postgres:18 



docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4

docker run -it --rm \
    --network=pipeline_default\
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=taxi_zone_pickup \
    --year=2025 \
    --month=11
Q3
SELECT count(1) FROM public.yellow_taxi_data_nov
where lpep_pickup_datetime between '2025-11-01' and '2025-12-01' and trip_distance <= 1;
Q4
SELECT lpep_pickup_datetime, trip_distance FROM public.yellow_taxi_data_nov
WHERE trip_distance < 100 order by trip_distance desc limit 1;

Q5
select "Zone" from taxi_zone_pickup where "LocationID" = (
select "PULocationID"  from yellow_taxi_data_nov group by "PULocationID" ORDER BY sum(total_amount) DESC Limit 1);

Q6
select "Zone" from taxi_zone_pickup where "LocationID" = (
select  ytdn."DOLocationID" as "dropoff" from yellow_taxi_data_nov ytdn
where ytdn."PULocationID" = (SELECT "LocationID" FROM taxi_zone_pickup  where "Zone" = 'East Harlem North') order by tip_amount desc limit 1)