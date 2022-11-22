# Unit 10 Homework: Surf’s Up

## Assignment Overview

I have decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, I did climate analysis on the area. The following sections outline the steps I did to accomplish this task:

### Part 1: Climate Analysis and Exploration 
![https://github.com/meena2203/sqlalchemy-challenge/blob/main/MR_climate_app.py]

In this section, I used Python and SQLAlchemy to perform basic climate analysis and data exploration of my climate database. Completed the following tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Used the provided [hawaii.sqlite](Resources/hawaii.sqlite) files to complete my climate analysis and data exploration.

* Used SQLAlchemy’s `create_engine` to connect to my SQLite database.

* Use SQLAlchemy’s `automap_base()` to reflect my tables into classes and saved a reference to those classes called `Station` and `Measurement`.

* Linked Python to the database by creating a SQLAlchemy session.

#### Precipitation Analysis

To perform an analysis of precipitation in the area, did the following:

* Found the most recent date in the dataset.

* Using this date, retrieved the previous 12 months of precipitation data by querying the 12 previous months of data. 

* Selected only the `date` and `prcp` values.

* Loaded the query results into a Pandas DataFrame, and set the index to the date column.

* Sorted the DataFrame values by `date`.

* Ploted the results by using the DataFrame `plot` method:
![recent_precipitation_data](https://user-images.githubusercontent.com/112845583/203435968-41ca4482-0b9b-4d78-927a-e143a754f6e1.png)

* Used Pandas to print the summary statistics for the precipitation data.
<img width="130" alt="precipitation_stats" src="https://user-images.githubusercontent.com/112845583/203436035-339fef88-a38d-4345-80b2-0535492be202.png">

#### Station Analysis

To perform an analysis of stations in the area, did the following:

* Designed a query to calculate the total number of stations in the dataset.

* Designed a query to find the most active stations (the stations with the most rows).

    * Listed the stations and observation counts in descending order.

    * Picked the first station in the list.

    * Using the most active station id, calculated the lowest, highest, and average temperatures (`func.min`, `func.max`, `func.avg`, and `func.count`).

 * Designed a query to retrieve the previous 12 months of temperature observation data (TOBS).

    * Filtered by the station with the highest number of observations.

    * Queried the previous 12 months of temperature observation data for this station.

    * Ploted the results as a histogram with `bins=12`:
    
    ![Temperature_histogram](https://user-images.githubusercontent.com/112845583/203436144-19e6d685-28c7-4aae-912b-8dd3f2584e2f.png)

 * Closed session.

- - -

### Part 2: 
Designing Climate App ![https://github.com/meena2203/sqlalchemy-challenge/blob/main/MR_climate_app.py]

After completing the initial analysis, designed a Flask API based on the above queries.

Used Flask to create routes, as follows:

* `/`

    * Homepage.

    * Listed all available routes.
    <img width="229" alt="Flask" src="https://user-images.githubusercontent.com/112845583/203437109-41ca2797-c13d-4ec0-9248-0571ddf2460a.png">

* `/api/v1.0/precipitation`

    * Converted the query results to a dictionary using `date` as the key and `prcp` as the value.

    * Returned the JSON representation of precipitation dictionary.

* `/api/v1.0/stations`

    * Returned a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

    * Queried the dates and temperature observations of the most active station for the previous year of data.

    * Returned a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

    * Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

    * When given the start only, calculated `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

    * When given the start and the end date, calculated the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).

#### Bonus Temperature Analysis 1 
![https://github.com/meena2203/sqlalchemy-challenge/blob/main/MR_temp_analysis_bonus_1.ipynb]

Conducted an analysis to answer the following question: Hawaii is reputed to enjoy mild weather all year round. Is there a meaningful difference between the temperatures in, for example, June and December?

* Used Pandas to perform the following steps:

    * Converted the date column format from `string` to `datetime`.

    * Set the date column as the DataFrame index.


* Identified the average temperature in June at all stations across all available years in the dataset. Did the same for the temperature in December.

* Used the t-test to determine whether the difference in means, if any, is statistically significant. 
<img width="927" alt="Analysis" src="https://user-images.githubusercontent.com/112845583/203436588-2c2697cd-a1d9-4c55-ae0f-f2f34d92cacc.png">

## References

Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, [https://doi.org/10.1175/JTECH-D-11-00103.1](https://doi.org/10.1175/JTECH-D-11-00103.1)

- - -

© 2022 edX Boot Camps LLC. Confidential and Proprietary. All Rights Reserved.
