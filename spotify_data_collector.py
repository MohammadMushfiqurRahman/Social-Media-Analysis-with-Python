import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Set your Spotify API credentials
client_id = 'e83364c68ff34996b30f762b459fa6fe'
client_secret = '336bede86c3b48dcb08ad2f3db5dec0d'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist_data(artist_name):
    """Get data for a specific artist"""
    # Search for the artist
    results = sp.search(q=f'artist:{artist_name}', type='artist')
    if not results['artists']['items']:
        print(f"No artist found with name: {artist_name}")
        return None
    
    # Get the first artist from the search results
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    artist_info = sp.artist(artist_id)
    
    # Get the artist's top tracks
    top_tracks = sp.artist_top_tracks(artist_id)
    
    return {
        'artist_info': artist_info,
        'top_tracks': top_tracks
    }

def get_track_geographic_data(track_id):
    """Simulate geographic data for a track (Spotify API doesn't directly provide geographic streaming data)"""
    # Note: This is a placeholder. Spotify doesn't provide public geographic streaming data through their API
    # In a real scenario, you would need to use Spotify for Artists or have special access
    
    # For demonstration purposes, we'll return None
    return None

def get_album_data(album_id):
    """Get data for a specific album"""
    album_info = sp.album(album_id)
    album_tracks = sp.album_tracks(album_id)
    
    return {
        'album_info': album_info,
        'album_tracks': album_tracks
    }

def collect_artist_discography(artist_name):
    """Collect all albums and tracks for an artist"""
    # Search for the artist
    results = sp.search(q=f'artist:{artist_name}', type='artist')
    if not results['artists']['items']:
        print(f"No artist found with name: {artist_name}")
        return None
    
    # Get the first artist from the search results
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    
    # Get all albums by the artist
    albums = []
    results = sp.artist_albums(artist_id, album_type='album')
    albums.extend(results['items'])
    
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    
    # Get all tracks from each album
    all_tracks = []
    for album in albums:
        # Get album tracks
        tracks = []
        results = sp.album_tracks(album['id'])
        tracks.extend(results['items'])
        
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        
        # Get audio features for each track
        track_ids = [track['id'] for track in tracks]
        
        # Process in batches of 50 (API limit)
        audio_features = []
        for i in range(0, len(track_ids), 50):
            batch = track_ids[i:i+50]
            audio_features.extend(sp.audio_features(batch))
            time.sleep(0.2)  # Avoid rate limiting
        
        # Combine track info with audio features
        for i, track in enumerate(tracks):
            if i < len(audio_features) and audio_features[i]:
                track_data = {
                    'track_id': track['id'],
                    'track_name': track['name'],
                    'album_name': album['name'],
                    'album_id': album['id'],
                    'release_date': album['release_date'] if 'release_date' in album else None,
                    'popularity': None,  # Need to call track endpoint for this
                    'duration_ms': track['duration_ms'],
                    **{k: audio_features[i][k] for k in audio_features[i] if k != 'type' and k != 'id' and k != 'track_href' and k != 'analysis_url'}
                }
                all_tracks.append(track_data)
    
    # Convert to DataFrame
    tracks_df = pd.DataFrame(all_tracks)
    return tracks_df

# Example usage
if __name__ == "__main__":
    artist_name = "Twice"  # Replace with your artist of interest
    
    print(f"Collecting data for {artist_name}...")
    tracks_df = collect_artist_discography(artist_name)
    
    if tracks_df is not None:
        print(f"Collected {len(tracks_df)} tracks")
        tracks_df.to_csv(f"{artist_name.replace(' ', '_')}_tracks.csv", index=False)
        print(f"Data saved to {artist_name.replace(' ', '_')}_tracks.csv")