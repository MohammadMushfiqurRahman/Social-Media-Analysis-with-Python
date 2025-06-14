# Social-Media-Analysis-with-Python

This repository contains two Python programs designed to collect and analyze Spotify data. The `spotify_data_collector.py` script retrieves detailed information about artists, albums, and tracks using the Spotify API, while the `spotify_geo_analysis.py` script analyzes the geographic distribution of Spotify streams and generates insights for marketing strategies.

## Program Overview

### Spotify Data Collector (`spotify_data_collector.py`)
The `spotify_data_collector.py` program interacts with the Spotify API to gather information about artists, their discographies, and tracks. It fetches artist details, their top tracks, and all albums, along with audio features for each track. The collected data is saved in a structured CSV format for further analysis.

#### Features:
- Collects artist data, including top tracks and discography.
- Retrieves detailed audio features like danceability, energy, and tempo for each track.
- Saves the collected data to a CSV file for easy analysis.

### Spotify Geo Analysis (`spotify_geo_analysis.py`)
The `spotify_geo_analysis.py` program visualizes the geographic distribution of Spotify streams by analyzing data from countries and cities. It generates interactive maps, heatmaps, and bar charts to display streaming activity and identifies both top-performing and underperforming regions. Based on these insights, the program generates actionable strategies to optimize content promotion.

#### Features:
- Visualizes streaming data across countries and cities with bar charts and maps.
- Creates heatmaps to identify high-traffic streaming areas.
- Identifies underperforming regions and provides strategies to increase engagement.
- Generates CSV files and reports with recommendations for marketing efforts.

## Prerequisites

Ensure that you have the following installed:
- Python 3.x
- Required libraries: `spotipy`, `pandas`, `matplotlib`, `seaborn`, `folium`, `geopandas`

To install the required dependencies, run:

```bash
pip install -r requirements.txt
