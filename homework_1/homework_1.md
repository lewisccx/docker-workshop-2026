# Homework 1: Docker, SQL and Terraform for Data Engineering Zoomcamp 2026#

### Q3
```
SELECT count(1) FROM public.yellow_taxi_data_nov
where lpep_pickup_datetime between '2025-11-01' and '2025-12-01' and trip_distance <= 1;
```
### Q4
```
SELECT lpep_pickup_datetime, trip_distance FROM public.yellow_taxi_data_nov
WHERE trip_distance < 100 order by trip_distance desc limit 1;
```
### Q5
```
select "Zone" from taxi_zone_pickup where "LocationID" = (
select "PULocationID"  from yellow_taxi_data_nov group by "PULocationID" ORDER BY sum(total_amount) DESC Limit 1);
```
### Q6
```
select "Zone" from taxi_zone_pickup where "LocationID" = (
select  ytdn."DOLocationID" as "dropoff" from yellow_taxi_data_nov ytdn
where ytdn."PULocationID" = (SELECT "LocationID" FROM taxi_zone_pickup  where "Zone" = 'East Harlem North') order by tip_amount desc limit 1)
```