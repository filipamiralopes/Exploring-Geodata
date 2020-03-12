# Exploring Geospatial data
Exploring Geodata and visualising it using GoogleMaps API.

## Data

I only attached a sample of the data.

- Radio Cell infrastructure (data/de_cells.csv): this data contains the location of the radio towers. The columns cid and area are together the uniq identifiers of the cell tower. The other two columns are the location.

- Events (data/00.csv): These events are snapshots of one device being in one location at a given time. The data consist of multiple CSV files with the following structure: imsi, imei, cell_id, tac, rac, sac, area_id, segment, ts_start, ts_end, erm, trf. The main fields which are relevant for this exercise:
  - imsi: subscriber identifier https://en.wikipedia.org/wiki/International_mobile_subscriber_identity
  - cell_id, area_id: unique identifier of a cell tower
  - ts_start, ts_end: signal start and end time


## Description

- Here I process the signalling information, join it with the cell information and visualize a few selected movement chains.
- Data processing involves parsing of the data, filtering the necessary columns and rows (data/00_treated.csv).
- To simulate a privacy step, I hash the imsi column with sha256 algorithm and use the resulting hexadecimal value.
- I'll be looking into only 4 signals.
- Based on the coordinates that can be found in the cell information, one can visualize the movement of these four subscribers (separately). For this I used GoogleMaps API and gmplot package (https://github.com/vgm64/gmplot)
