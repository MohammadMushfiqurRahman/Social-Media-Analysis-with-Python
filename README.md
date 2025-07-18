﻿# Social-Media-Analysis-with-Python

This repository contains two Python programs designed to collect and analyse Spotify data. The `spotify_data_collector.py` script retrieves detailed information about artists, albums, and tracks using the Spotify API, while the `spotify_geo_analysis.py` script analyzes the geographic distribution of Spotify streams and generates insights for marketing strategies.

## Program Overview

### Spotify Data Collector (`spotify_data_collector.py`)
The `spotify_data_collector.py` program interacts with the Spotify API to gather information about artists, their discographies, and tracks. It fetches artist details, their top tracks, and all albums, along with audio features for each track. The collected data is saved in a structured CSV format for further analysis.

## Features

* **Artist Discography Collection**: Fetches all albums and tracks for a specified artist from Spotify.
* **Audio Features Integration**: Gathers audio features (e.g., danceability, energy) for each track.
* **Simulated Geographic Streaming Data**: Generates realistic sample geographic streaming data since Spotify's public API does not provide this information directly.
* **Geographic Distribution Analysis**: Visualises streaming distribution by country and city using bar charts, interactive Folium maps, and heatmaps.
* **Hotspot Identification**: Pinpoints top-performing countries and cities.
* **Underperforming Region Detection**: Identifies regions with streaming numbers below a defined threshold.
* **Actionable Strategy Generation**: Provides tailored strategies for both high-performing and underperforming regions.

## Files

* `spotify_data_collector.py`: Python script responsible for collecting artist discography data from the Spotify API.
* `spotify_geo_analysis.py`: Python script for performing geographic analysis and generating strategies, utilising either collected data or simulated data.

## Setup

### Prerequisites

* Python 3.x
* A Spotify Developer account to obtain API credentials.

### Spotify API Credentials

1.  Go to the [Spotify for Developers Dashboard](https://developer.spotify.com/dashboard/).
2.  Log in with your Spotify account.
3.  Click "Create an app" to create a new application.
4.  Fill in the app details. For the "Redirect URI", you can use `http://localhost:8888/` for local development, but be aware that Spotify recommends using `https` for production applications.
5.  Once your app is created, you will find your `Client ID` and `Client Secret`.

Update the `client_id` and `client_secret` variables in `spotify_data_collector.py` with your credentials:

```python
# Set your Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
