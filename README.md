# CommSquare_assignment
Components:

1. Data Ingestion:

Responsible for ingesting raw data from CSV files.
Monitors the designated folder for new files.
Parses and validates the CSV data.
Data Processing:

2. Processes the raw data to calculate the required KPIs.
Aggregates data based on the specified intervals (5-minute and 1-hour).
Identifies top services and cells as per KPI definitions.
Creates records for each KPI.
3. Database Storage:

Stores the calculated KPIs in the database.
Two separate tables for each KPI (KPI1 and KPI2).
Tables have fields based on the KPI definitions.
4. Scheduler:

Triggers the data processing at regular intervals (every 5 minutes).
Runs hourly jobs for 1-hour intervals.
5. Logging:

Captures logs for data processing steps, errors, and system events.
Useful for monitoring and debugging.
6. Configuration Management:

Stores configuration parameters, such as file paths, database connections, and interval definitions.
Interactions:

Data Ingestion → Data Processing:

Data Ingestion triggers Data Processing when new CSV files are detected.
Passes the parsed data to the Data Processing component.
Data Processing → Database Storage:

Data Processing creates records for KPI1 and KPI2.
Sends the records to the Database Storage component for storage.
Scheduler → Data Processing:

Scheduler triggers Data Processing at regular intervals (every 5 minutes).

Runs hourly jobs for 1-hour intervals.
Data Processing → Logging:

Logs events, errors, and processing details for monitoring and debugging purposes.
Configuration Management → Data Ingestion, Data Processing, Database Storage:

Provides configuration parameters to these components.


+---------------------+     +------------------------+     +------------------+
|    Data Ingestion   | --> |    Data Processing     | --> | Database Storage |
+---------------------+     +------------------------+     +------------------+
        |                               |                             |
        |                               |                             |
	|				|			      |
	|				|			      |
	|			+-------------+			      |
        |-----------------------|  Scheduler  |-----------------------|
                                +-------------+
					|
					|
                	         +-------------+
                                 |   Logging   |
                                 +-------------+
					|
					|
			       +------------------+ 
			       |  Configuration   |
			       +------------------+       
