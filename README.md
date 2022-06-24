### Introduction
This project provides insights about stakepool operator data using Cardano db-sync data as source of truth. 

### Goals
Primary goals for this project include
  - base SQL scripts and core scripts to answer most important question about stakepool data
  - python scripts to extract and integrate extended metadata into Postgres
  - python scripts to load extended metadata into s3
  - python scripts to extract and load stakepool aggregate data into s3

### Non-Goals
This project does not provide 
  - steps to set up dbsync
  - any insights into transactional datasets
  - scheduling or hosted data service

### Prerequisites
  - up and running instance which hosts db-sync
  - environment variables setup
  - pyenv (this project uses python3.8.9) - https://github.com/pyenv/pyenv
  - poetry - https://python-poetry.org/

### Exporting environment variables
Please run the following commands before running any python script
- export db_host= << your dbsync host >> # if you're using jumphost this will be localhost
- export db_name= << your dbsync database name> >
- export db_username= << dbsync username >>
- export db_password= << dbsync password >>
- export AWS_ACCESS_KEY_ID= << aws access key >>
- export AWS_SECRET_ACCESS_KEY= << aws secret key >>

### Formating and Linting

run following command to test for any linting errors
 
 `poetry run pylint lib` 
 
 `poetry run pylint stakepool_metadata`

run following command to test for any SQL lint errors
 
 `poetry run sqlfluff lint resources/`

run the following commands to fix any fixable formating of SQL resources
 
 `poetry run sqlfluff fix resources` 

### Developer set up

If you are a developer you might want to go through following steps to get started
- set up dbsync using the following guide 
https://cardano-community.github.io/guild-operators/Build/dbsync/
- clone the project using following command
`git clone git@github.com:Cardano-Data-Hub/cardano-stake-pool-analytics-dataset-internal.git`
- In SQL explorer of your choice, run the SQL scripts from base_views.sql which can be found under resources/intermediate path

### Extract stakepool metadata
The stakepool metadata consists of following information
- json extracts of extended metadata
- structured csv data for stakepool socials
- structured csv data for stakepool itn/owner information

Before exporting stakepool metadata to s3 the data first needs to be ingested and integrated in postgres. This can be accomplished using following command
`poetry run python stakepool_operations/ingest_metadata.py`

After this step is successfully executed you can run the following command to extract data to s3
`poetry run python stakepool_operations/extract_metadata.py`

### Extract stakepool kpis
Based on the stakepool data collected so far we were able to identify key KPIs for stakepool operations. Following KPIs are sliced by pools and interval parameter. An interval parameter is a range of time specified in epoch, month or year.

- Attrition -> Count and Change of pools retiring during an epoch, month and year
- Growth -> Count and change of newly added pools during an epoch, month and year
- Performance 
  - Performance by amount of Ada delegated -> Count and change of ada delegations to a pool by epoch, month and year
  - Performance by wallet delegates -> Count and change of new wallet delegations to a pool by epoch, month and year

The following KPI or data points are not defined on a longer term interval and are only available by epoch
- Pledge vs ROA -> What is the pools performance in terms of its pledge (only available by epoch)
- Effect of changing pool parameter -> This looks into how changing pool parameters affect performance of a specific pool over time (only available by epoch)

To extract KPIs with the interval run the following command
`poetry run python stakepool_operations/etl_kpis <kpi_name> --interval <interval>`
- interval can take only three values from (epoch, monthly and yearly)
- following kpi names are available with this release
  - attrition_rate
  - growth_rate
  - performance 
  - pledge_vs_roa
  - pool_parameters

Example
- To extract kpi for monthly attrition rate run
`poetry run python stakepool_operations/etl_kpis attrition_rate --interval monthly`
Note: Not providing interval will default to epoch

- For extracting non interval data points like pool parameter run
`poetry run python stakepool_operations/etl_kpis pool_parameters`
