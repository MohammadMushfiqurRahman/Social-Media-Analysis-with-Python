import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from shapely.geometry import Point
import random
from matplotlib.colors import LinearSegmentedColormap

# Set the visual style for plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


class SpotifyGeoAnalysis:
    def __init__(self, data_path=None):
        """
        Initialize the analysis with either a data path or generate sample data
        """
        if data_path:
            self.df = pd.read_csv(data_path)
        else:
            self.df = self._generate_sample_data()
        
        # Set threshold for underperforming regions
        self.underperforming_threshold = 50000
        
    def _generate_sample_data(self):
        """
        Generate sample streaming data for demonstration purposes
        """
        # List of countries and major cities
        countries = ['USA', 'UK', 'Brazil', 'Japan', 'Germany', 'France', 'Australia', 
                    'Canada', 'Mexico', 'India', 'South Korea', 'Spain', 'Italy', 
                    'Netherlands', 'Sweden', 'Argentina', 'Colombia', 'South Africa', 
                    'Nigeria', 'Egypt', 'Russia', 'China', 'Indonesia']
        
        cities = {
            'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'],
            'UK': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Liverpool'],
            'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza'],
            'Japan': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama', 'Sapporo'],
            'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne'],
            'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
            'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'Mexico': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana'],
            'India': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
            'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon'],
            'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
            'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'],
            'Sweden': ['Stockholm', 'Gothenburg', 'Malmö', 'Uppsala', 'Västerås'],
            'Argentina': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata'],
            'Colombia': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena'],
            'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth'],
            'Nigeria': ['Lagos', 'Kano', 'Ibadan', 'Abuja', 'Port Harcourt'],
            'Egypt': ['Cairo', 'Alexandria', 'Giza', 'Shubra El-Kheima', 'Port Said'],
            'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'],
            'China': ['Beijing', 'Shanghai', 'Guangzhou', 'Shenzhen', 'Chengdu'],
            'Indonesia': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang']
        }
        
        # Coordinates (approximate) for each country
        country_coords = {
            'USA': (37.0902, -95.7129),
            'UK': (55.3781, -3.4360),
            'Brazil': (-14.2350, -51.9253),
            'Japan': (36.2048, 138.2529),
            'Germany': (51.1657, 10.4515),
            'France': (46.2276, 2.2137),
            'Australia': (-25.2744, 133.7751),
            'Canada': (56.1304, -106.3468),
            'Mexico': (23.6345, -102.5528),
            'India': (20.5937, 78.9629),
            'South Korea': (35.9078, 127.7669),
            'Spain': (40.4637, -3.7492),
            'Italy': (41.8719, 12.5674),
            'Netherlands': (52.1326, 5.2913),
            'Sweden': (60.1282, 18.6435),
            'Argentina': (-38.4161, -63.6167),
            'Colombia': (4.5709, -74.2973),
            'South Africa': (-30.5595, 22.9375),
            'Nigeria': (9.0820, 8.6753),
            'Egypt': (26.8206, 30.8025),
            'Russia': (61.5240, 105.3188),
            'China': (35.8617, 104.1954),
            'Indonesia': (-0.7893, 113.9213)
        }
        
        # City coordinates (approximate)
        city_coords = {
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'London': (51.5074, -0.1278),
            'Tokyo': (35.6762, 139.6503),
            'Paris': (48.8566, 2.3522),
            'São Paulo': (-23.5505, -46.6333),
            'Berlin': (52.5200, 13.4050),
            'Sydney': (-33.8688, 151.2093),
            'Toronto': (43.6511, -79.3470),
            'Mexico City': (19.4326, -99.1332),
            'Mumbai': (19.0760, 72.8777),
            'Seoul': (37.5665, 126.9780),
            'Madrid': (40.4168, -3.7038),
            'Rome': (41.9028, 12.4964),
            'Amsterdam': (52.3676, 4.9041),
            'Stockholm': (59.3293, 18.0686),
            'Buenos Aires': (-34.6037, -58.3816),
            'Bogotá': (4.7110, -74.0721),
            'Johannesburg': (-26.2041, 28.0473),
            'Lagos': (6.5244, 3.3792),
            'Cairo': (30.0444, 31.2357),
            'Moscow': (55.7558, 37.6173),
            'Beijing': (39.9042, 116.4074),
            'Jakarta': (-6.2088, 106.8456)
        }
        
        # For cities without specific coordinates, generate approximate ones based on country
        for country, city_list in cities.items():
            country_lat, country_lon = country_coords[country]
            for city in city_list:
                if city not in city_coords:
                    # Add some random offset to the country coordinates
                    city_coords[city] = (
                        country_lat + random.uniform(-2, 2),
                        country_lon + random.uniform(-2, 2)
                    )
        
        # Generate sample data
        data = []
        
        # Create a distribution that favors certain countries/cities
        # to simulate real-world streaming patterns
        country_popularity = {
            'USA': 100,
            'UK': 85,
            'Brazil': 90,
            'Japan': 75,
            'Germany': 80,
            'France': 70,
            'Australia': 65,
            'Canada': 75,
            'Mexico': 60,
            'India': 85,
            'South Korea': 95,
            'Spain': 60,
            'Italy': 55,
            'Netherlands': 50,
            'Sweden': 65,
            'Argentina': 45,
            'Colombia': 40,
            'South Africa': 35,
            'Nigeria': 30,
            'Egypt': 25,
            'Russia': 40,
            'China': 70,
            'Indonesia': 55
        }
        
        # Generate data for each country and its cities
        for country in countries:
            country_base = country_popularity[country] * 1000
            
            # Add country-level data
            country_streams = int(country_base * random.uniform(0.8, 1.2))
            lat, lon = country_coords[country]
            
            data.append({
                'country': country,
                'city': 'All',
                'streams': country_streams,
                'latitude': lat,
                'longitude': lon
            })
            
            # Add city-level data
            for city in cities[country]:
                # Cities get a portion of the country's streams with some randomness
                city_factor = random.uniform(0.1, 0.5)
                city_streams = int(country_streams * city_factor)
                
                lat, lon = city_coords[city]
                
                data.append({
                    'country': country,
                    'city': city,
                    'streams': city_streams,
                    'latitude': lat,
                    'longitude': lon
                })
        
        return pd.DataFrame(data)
    
    def analyze_geographic_distribution(self):
        """
        Analyze and visualize the geographic distribution of streams
        """
        # Group by country and sum streams
        country_streams = self.df[self.df['city'] != 'All'].groupby('country')['streams'].sum().reset_index()
        country_streams = country_streams.sort_values('streams', ascending=False)
        
        # Create a bar chart for countries
        plt.figure(figsize=(14, 8))
        sns.barplot(x='country', y='streams', data=country_streams)
        plt.title('Total Streams by Country', fontsize=16)
        plt.xlabel('Country', fontsize=14)
        plt.ylabel('Number of Streams', fontsize=14)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('country_streams.png')
        plt.close()
        
        # Create a world map visualization
        world_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        
        # Add circles for each country
        for _, row in country_streams.iterrows():
            country_data = self.df[(self.df['country'] == row['country']) & (self.df['city'] == 'All')].iloc[0]
            
            # Scale the radius based on the number of streams
            radius = np.sqrt(row['streams']) / 30
            
            folium.Circle(
                location=[country_data['latitude'], country_data['longitude']],
                radius=radius,
                popup=f"{row['country']}: {row['streams']:,} streams",
                color='crimson',
                fill=True,
                fill_color='crimson'
            ).add_to(world_map)
        
        # Save the map
        world_map.save('world_streams_map.html')
        
        # Create a heatmap
        heat_data = []
        for _, row in self.df[self.df['city'] != 'All'].iterrows():
            heat_data.append([row['latitude'], row['longitude'], row['streams']/10000])
        
        heatmap_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        HeatMap(heat_data).add_to(heatmap_map)
        heatmap_map.save('streams_heatmap.html')
        
        return country_streams
    
    def identify_regional_hotspots(self):
        """
        Identify and visualize regional hotspots
        """
        # Top countries
        top_countries = self.df[self.df['city'] == 'All'].sort_values('streams', ascending=False).head(10)
        
        # Top cities overall
        top_cities = self.df[self.df['city'] != 'All'].sort_values('streams', ascending=False).head(20)
        
        # Create visualizations
        fig, axes = plt.subplots(2, 1, figsize=(14, 16))
        
        # Top countries
        sns.barplot(x='country', y='streams', data=top_countries, ax=axes[0], palette='viridis')
        axes[0].set_title('Top 10 Countries by Streams', fontsize=16)
        axes[0].set_xlabel('Country', fontsize=14)
        axes[0].set_ylabel('Number of Streams', fontsize=14)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Top cities
        sns.barplot(x='city', y='streams', data=top_cities, ax=axes[1], palette='viridis')
        axes[1].set_title('Top 20 Cities by Streams', fontsize=16)
        axes[1].set_xlabel('City', fontsize=14)
        axes[1].set_ylabel('Number of Streams', fontsize=14)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('regional_hotspots.png')
        plt.close()
        
        # Create a map of top cities
        hotspot_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        
        # Add markers for top cities
        for _, row in top_cities.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['city']}, {row['country']}: {row['streams']:,} streams",
                icon=folium.Icon(color='green', icon='play', prefix='fa')
            ).add_to(hotspot_map)
        
        hotspot_map.save('hotspot_cities_map.html')
        
        return top_countries, top_cities
    
    def identify_underperforming_regions(self):
        """
        Identify regions with streams below the threshold
        """
        # Find underperforming countries
        underperforming_countries = self.df[
            (self.df['city'] == 'All') & 
            (self.df['streams'] < self.underperforming_threshold)
        ].sort_values('streams')
        
        # Find underperforming cities in otherwise well-performing countries
        country_avg = self.df[self.df['city'] != 'All'].groupby('country')['streams'].mean().reset_index()
        country_avg = country_avg.rename(columns={'streams': 'avg_streams'})
        
        # Merge with city data
        city_data = self.df[self.df['city'] != 'All'].merge(country_avg, on='country')
        
        # Find cities that are below average for their country
        underperforming_cities = city_data[
            (city_data['streams'] < city_data['avg_streams'] * 0.5) &
            (city_data['streams'] < self.underperforming_threshold)
        ].sort_values('streams')
        
        # Visualize underperforming regions
        if not underperforming_countries.empty:
            plt.figure(figsize=(14, 8))
            sns.barplot(x='country', y='streams', data=underperforming_countries)
            plt.title('Underperforming Countries (Below Threshold)', fontsize=16)
            plt.xlabel('Country', fontsize=14)
            plt.ylabel('Number of Streams', fontsize=14)
            plt.axhline(y=self.underperforming_threshold, color='r', linestyle='--', 
                        label=f'Threshold ({self.underperforming_threshold:,} streams)')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('underperforming_countries.png')
            plt.close()
        
        # Create a map of underperforming regions
        underperform_map = folium.Map(location=[20, 0], zoom_start=2, tiles='CartoDB positron')
        
        # Add markers for underperforming countries
        for _, row in underperforming_countries.iterrows():
            folium.Circle(
                location=[row['latitude'], row['longitude']],
                radius=200000,  # Fixed size for visibility
                popup=f"{row['country']}: {row['streams']:,} streams",
                color='red',
                fill=True,
                fill_color='red'
            ).add_to(underperform_map)
        
        # Add markers for underperforming cities
        for _, row in underperforming_cities.iterrows():
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=f"{row['city']}, {row['country']}: {row['streams']:,} streams",
                icon=folium.Icon(color='red', icon='volume-down', prefix='fa')
            ).add_to(underperform_map)
        
        underperform_map.save('underperforming_regions_map.html')
        
        return underperforming_countries, underperforming_cities
    
    def generate_actionable_strategies(self):
        """
        Generate actionable strategies based on the analysis
        """
        # Get top performing regions
        top_countries, top_cities = self.identify_regional_hotspots()
        
        # Get underperforming regions
        underperforming_countries, underperforming_cities = self.identify_underperforming_regions()
        
        # Create strategy dataframes
        high_performing_strategies = []
        for _, row in top_countries.head(5).iterrows():
            strategies = [
                f"Schedule tour dates in {row['country']}",
                f"Create exclusive content for {row['country']} fans",
                f"Partner with local brands in {row['country']}",
                f"Increase social media engagement targeting {row['country']}"
            ]
            high_performing_strategies.append({
                'region': row['country'],
                'streams': row['streams'],
                'strategy': random.choice(strategies)
            })
        
        for _, row in top_cities.head(10).iterrows():
            strategies = [
                f"Host fan meetup in {row['city']}",
                f"Collaborate with local artists from {row['city']}",
                f"Target radio promotion in {row['city']}",
                f"Create city-specific merchandise for {row['city']}"
            ]
            high_performing_strategies.append({
                'region': f"{row['city']}, {row['country']}",
                'streams': row['streams'],
                'strategy': random.choice(strategies)
            })
        
        low_performing_strategies = []
        for _, row in underperforming_countries.iterrows():
            strategies = [
                f"Collaborate with top artist from {row['country']}",
                f"Create localized content for {row['country']} audience",
                f"Partner with influencers in {row['country']}",
                f"Run targeted ads in {row['country']}"
            ]
            low_performing_strategies.append({
                'region': row['country'],
                'streams': row['streams'],
                'strategy': random.choice(strategies)
            })
        
        for _, row in underperforming_cities.head(15).iterrows():
            strategies = [
                f"Partner with local radio stations in {row['city']}",
                f"Collaborate with local influencers from {row['city']}",
                f"Create targeted social media campaigns for {row['city']}",
                f"Offer exclusive content for {row['city']} listeners"
            ]
            low_performing_strategies.append({
                'region': f"{row['city']}, {row['country']}",
                'streams': row['streams'],
                'strategy': random.choice(strategies)
            })
        
        # Convert to dataframes
        high_df = pd.DataFrame(high_performing_strategies)
        low_df = pd.DataFrame(low_performing_strategies)
        
        # Save strategies to CSV
        if not high_df.empty:
            high_df.to_csv('high_performing_strategies.csv', index=False)
        if not low_df.empty:
            low_df.to_csv('low_performing_strategies.csv', index=False)
        
        # Create a comprehensive strategy report
        with open('strategy_report.md', 'w') as f:
            f.write("# Streaming Performance Strategy Report\n\n")
            
            f.write("## High-Performing Regions Strategies\n\n")
            f.write("| Region | Streams | Recommended Strategy |\n")
            f.write("|--------|---------|----------------------|\n")
            for _, row in high_df.iterrows():
                f.write(f"| {row['region']} | {row['streams']:,} | {row['strategy']} |\n")
            
            f.write("\n## Underperforming Regions Strategies\n\n")
            f.write("| Region | Streams | Recommended Strategy |\n")
            f.write("|--------|---------|----------------------|\n")
            for _, row in low_df.iterrows():
                f.write(f"| {row['region']} | {row['streams']:,} | {row['strategy']} |\n")
        
        return high_df, low_df
    
    def run_full_analysis(self):
        """
        Run the complete analysis pipeline
        """
        print("Starting geographic streaming data analysis...")
        
        print("\nAnalyzing geographic distribution...")
        country_streams = self.analyze_geographic_distribution()
        print(f"Analysis complete. Top country: {country_streams.iloc[0]['country']} with {country_streams.iloc[0]['streams']:,} streams")
        
        print("\nIdentifying regional hotspots...")
        top_countries, top_cities = self.identify_regional_hotspots()
        print(f"Found {len(top_countries)} top countries and {len(top_cities)} top cities")
        
        print("\nIdentifying underperforming regions...")
        underperforming_countries, underperforming_cities = self.identify_underperforming_regions()
        print(f"Found {len(underperforming_countries)} underperforming countries and {len(underperforming_cities)} underperforming cities")
        
        print("\nGenerating actionable strategies...")
        high_strategies, low_strategies = self.generate_actionable_strategies()
        print(f"Generated {len(high_strategies)} strategies for high-performing regions")
        print(f"Generated {len(low_strategies)} strategies for underperforming regions")
        
        print("\nAnalysis complete! Results saved to files:")
        print("- country_streams.png - Bar chart of streams by country")
        print("- world_streams_map.html - Interactive map of streams by country")
        print("- streams_heatmap.html - Heatmap of streaming activity")
        print("- regional_hotspots.png - Bar charts of top countries and cities")
        print("- hotspot_cities_map.html - Interactive map of top cities")
        print("- underperforming_countries.png - Bar chart of underperforming countries")
        print("- underperforming_regions_map.html - Interactive map of underperforming regions")
        print("- high_performing_strategies.csv - Strategies for high-performing regions")
        print("- low_performing_strategies.csv - Strategies for underperforming regions")
        print("- strategy_report.md - Comprehensive strategy report")


# Example usage
if __name__ == "__main__":
    # Initialize the analyzer with sample data
    # You can replace this with your actual data file path
    analyzer = SpotifyGeoAnalysis()
    
    # Run the full analysis
    analyzer.run_full_analysis()