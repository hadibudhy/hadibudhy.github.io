# Data sources

| Source | Organization | Use | Provenance and limitation |
|---|---|---|---|
| [Criteo Uplift Prediction Dataset](https://ailab.criteo.com/criteo-uplift-prediction-dataset/) | Criteo AI Lab | Randomized campaign incrementality | Unbiased v2.1 release, 13,979,592 rows, CC BY-NC-SA 4.0; anonymized features and no campaign economics |
| [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) | NYC Taxi and Limousine Commission | HVFHV marketplace and congestion analysis | Submitted trip records; each row is one dispatched trip; requests, lost matches, and driver online time are not observed |
| [HVFHV data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf) | NYC TLC | Field definitions and grain | States that each row is one trip and identifies high-volume license groups |
| [NYC Open Data 2019 HVFHV table](https://data.cityofnewyork.us/Transportation/2019-High-Volume-FHV-Trip-Records/4p5c-cbgn) | NYC TLC / NYC Open Data | Bounded API slice for supply-demand project | Historical table with seven trip fields and unspecified license terms |
| [TLC monthly data reports](https://www.nyc.gov/site/tlc/about/aggregated-reports.page) | NYC TLC | Observed monthly supply proxies and trip trends | Includes High Volume FHV trips per day, unique drivers, unique vehicles, vehicles per day, average hours, and average trip minutes; not an hourly request or online-supply feed |
| [MTA CBD geofence](https://data.ny.gov/widgets/srxy-5nxn?mobile_redirect=true) | New York State / MTA | Reproducible congestion-zone boundary | Machine-readable polygons; excluded-roadway and through-route rules still require trip-level validation |
| [MTA Congestion Relief Zone Vehicle Entries](https://data.ny.gov/) | New York State / MTA | External traffic triangulation | Hourly/10-minute crossing counts by vehicle class; not a measure of HVFHV requests or driver supply |
| [MTA Bridges and Tunnels Hourly Crossings](https://catalog.data.gov/dataset/mta-bridges-and-tunnels-hourly-crossings-beginning-2019) | New York State / MTA | Empirical congestion-policy outcome | Facility, direction, vehicle class, and payment method; used here as daily car counts for a transparent event-study audit |
