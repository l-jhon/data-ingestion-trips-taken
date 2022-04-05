# Data Engineering Challenge

## Description

This challenge will evaluate your proficiency in Data Engineering, and your knowledge in
Software development as well.

## Assignment

Your task is to build an automatic process to ingest data on an on-demand basis. The data
represents trips taken by different vehicles, and include a city, a point of origin and a destination.
This CSV file gives you a small sample of the data your solution will have to handle. We would
like to have some visual reports of this data, but in order to do that, we need the following
features.
We do not need a graphical interface. Your application should preferably be a REST API, or a
console application.

## Mandatory Features

- [x] There must be an automated process to ingest and store the data.
- [x] Trips with similar origin, destination, and time of day should be grouped together.
- [x] Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region.
- [x] Develop a way to inform the user about the status of the data ingestion without using a polling solution.
- [x] The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable.
- [x] Use a SQL database.

## Bonus features

- [x] Containerize your solution.
- [x] Sketch up how you would set up the application using any cloud provider (AWS, Google Cloud, etc).
- [x] Include a .sql file with queries to answer these questions:
- [x] From the two most commonly appearing regions, which is the latest datasource?
- [x] What regions has the "cheap_mobile" datasource appeared in?

## Deliverables

Your project should be stored in a public GitHub repository. When you are done, send us the link
to your repo.
It’s not necessary to host this application anywhere (although you can if you like). Just make
sure your repo has a README.md which contains any instructions we might need for running
your project.

Observations/Recommendation
● If you will integrate your solution with any cloud platform, you must provide an account
(user/password) to us to test it.
● Please detail your code so that we can understand your reasoning and its use regardless
of platform expertise.
● We recommend recording a video explaining how it works and steps of execution.

## Challenge Results

For this challenge, a data ingestion pipeline was developed using Python, Redis as Queue and PostgreSQL as SQL Database.

This architecture was chosen because we need to think in scalability, and
using Redis as a Queue, we can receive a lot of entries and send it to SQL Database. In production environment we can substitute the Redis for a Kafka, Kinesis or another pub/sub service that is available in cloud providers. Using services like that, we can scalable by infinite, and then the solution can receive more than 100 million entries.

In this project we used docker to deploy some services to run the project in the local environment, and this is great because you can run this code in any environment you want, just install ```docker``` and ```docker-compose```.

### Data Ingestion Pipeline:

![Alt text](docs/pipeline_docker_compose.png?raw=true "Data Ingestion Pipeline")

### Executing Local - Development Enviroment - Data Ingestion
Execute the data ingestion local using only poetry virtual env. In this case we need to create PostgreSQL and Redis service to execute the data ingestion, because this is a requirement to execute the project.

Data Ingestion:
```
cd infra/local/dev && ./create_services.sh
cd - &
```

### Executing Local - Production Enviroment - Data Ingestion
In this case we can using docker-compose to create all services we need to execute the data ingestion pipeline, include PostgreSQL Database, Redis to Queed and Python App, the main part of this project.

This option is with all services deployed using Containers.

Steps:
```
docker-compose exec python_app python main.py --file data/<file_name>
```

### Getting the answers to the questions

What is the weekly average number of trips for an area, defined by a
bounding box (given by coordinates) or by a region?
```
python main.py --metric weekly

# SQL Query
cat resources/sql/weekly_average_trips.sql
```

From the two most commonly appearing regions, which is the latest datasource?
```
python main.py --metric commonly

# SQL Query
cat resources/sql/latest_datasource_commonly_region.sql
```

What regions has the "cheap_mobile" datasource appeared in?
```
python main.py --metric cheap_mobile

# SQL Query
cat resources/sql/number_of_appearances.sql
```

### Set up the application using AWS Cloud

![Alt text](docs/aws.png?raw=true "AWS Cloud")

Notes:
* This solution in AWS is scalable, mostly in the ```option 1``` for message or streaming layer using Kinesis, because this services is serveless, and in this case we dont need worry about computer resources, AWS care of this for us, Amazon Kinesis is a managed service.
* The ```option 2``` in this flow using Kafka on AWS, is a great service to using to, but in this case we need to worry about number of nodes, about computer resources, retetion policies.
* This designed solution is intended to be scalable, providing the end user with a great solution to perform massive data ingestion and data analysis in real time or in batch if the user does not need the data in real time.
* In this solution we have a Lambda Architecture, where we can have batch processing and streaming processing, to give all the necessary analytical support to users, so that they can make decisions based on data.


## Notes

* The user can see the running status through the logs that are generated in the console.
* The data was stored in the PostgreSQL Database following the instructions on grouping similar trips, in this case it was only possible to group by time, value extracted from the datetime column.
* Script to create table and partitions:
  ```
  cd resources/ddl/ && cat create_table_trips.sql
  ```

## Improvements
* Deploy this solution on cloud using Terraform as solution for infra as code
* Refactor the log messages, change the method to show the user what the status of data ingestion is.
* Add CI/CD Pipeline to automate the deploy
* Add Data Quality in data pipeline
* Add Unit test to assure the quality of the data and code.
* Improve table partitioning in SQL Database, to use origin_coord and destination_coord to group similar data.

