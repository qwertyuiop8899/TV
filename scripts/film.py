#!/usr/bin/env python3
"""
TMDB M3U Playlist Generator
Fetches movies from TMDB API and creates an M3U playlist with vixsrc.to links
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
import hashlib

# Load environment variables
load_dotenv()

class TMDBM3UGenerator:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"
        self.vixsrc_base = "https://vixsrc.to/movie"
        self.vixsrc_api = "https://vixsrc.to/api/list/movie/?lang=it"

        # Definisce il percorso di base per i file di output (la cartella genitore dello script)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.dirname(script_dir)
        self.cache_file = os.path.join(script_dir, "film_cache.json")
        self.cache = self._load_cache()
        self.vixsrc_movies = self._load_vixsrc_movies()
        
        if not self.api_key:
            raise ValueError("TMDB_API_KEY environment variable is required")
    
    def _load_vixsrc_movies(self):
        """Load available movies from vixsrc.to API"""
        try:
            print("Loading vixsrc.to movie list...")
            response = requests.get(self.vixsrc_api, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Extract tmdb_ids from the response
            vixsrc_ids = set()
            for item in data:
                if item.get('tmdb_id') and item['tmdb_id'] is not None:
                    vixsrc_ids.add(str(item['tmdb_id']))
            
            print(f"Loaded {len(vixsrc_ids)} available movies from vixsrc.to")
            return vixsrc_ids
        except Exception as e:
            print(f"Warning: Could not load vixsrc.to movie list: {e}")
            print("Continuing without vixsrc.to verification...")
            return set()
    
    def _is_movie_available_on_vixsrc(self, tmdb_id):
        """Check if movie is available on vixsrc.to"""
        return str(tmdb_id) in self.vixsrc_movies
    
    def _load_cache(self):
        """Load existing cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                print(f"Loaded cache with {len(cache)} movies")
                return cache
            except Exception as e:
                print(f"Error loading cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            print(f"Cache saved with {len(self.cache)} movies")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def _get_cache_key(self, movie):
        """Generate cache key for a movie"""
        return str(movie['id'])
    
    def _is_movie_cached(self, movie):
        """Check if movie is already in cache"""
        cache_key = self._get_cache_key(movie)
        return cache_key in self.cache
    
    def _add_to_cache(self, movie):
        """Add movie to cache"""
        cache_key = self._get_cache_key(movie)
        self.cache[cache_key] = {
            'id': movie['id'],
            'title': movie['title'],
            'release_date': movie.get('release_date', ''),
            'vote_average': movie.get('vote_average', 0),
            'poster_path': movie.get('poster_path', ''),
            'genre_ids': movie.get('genre_ids', []),
            'cached_at': datetime.now().isoformat()
        }
    
    def get_popular_movies(self, page=1, language='it-IT'):
        """Fetch popular movies from TMDB"""
        url = f"{self.base_url}/movie/popular"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': language
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_top_rated_movies(self, page=1, language='it-IT'):
        """Fetch top rated movies from TMDB"""
        url = f"{self.base_url}/movie/top_rated"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': language
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_all_movies(self, page=1, language='it-IT'):
        """Fetch all movies from TMDB (discover endpoint)"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': language,
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'include_video': False
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_movie_genres(self):
        """Fetch movie genres from TMDB"""
        url = f"{self.base_url}/genre/movie/list"
        params = {
            'api_key': self.api_key,
            'language': 'it-IT'
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return {genre['id']: genre['name'] for genre in response.json()['genres']}
    
    def get_latest_movies(self, page=1, language='it-IT'):
        """Fetch latest movies from TMDB"""
        url = f"{self.base_url}/movie/now_playing"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': language
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def generate_m3u_playlist(self, movies_data, output_file="tmdb_movies.m3u"):
        """Generate M3U playlist from movies data"""
        # Get genres mapping
        genres = self.get_movie_genres()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write M3U header
            f.write("#EXTM3U\n")
            f.write(f"# Generated by TMDB M3U Generator on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Total movies: {len(movies_data)}\n\n")
            
            for movie in movies_data:
                tmdb_id = movie['id']
                title = movie['title']
                year = movie.get('release_date', '')[:4] if movie.get('release_date') else ''
                
                # Get rating and create stars
                rating = movie.get('vote_average', 0)
                stars = "★" * int(rating / 2) + "☆" * (5 - int(rating / 2)) if rating > 0 else "☆☆☆☆☆"
                
                # Get all genres
                genre_names = []
                if movie.get('genre_ids') and movie['genre_ids']:
                    for genre_id in movie['genre_ids']:
                        genre_name = genres.get(genre_id, "")
                        if genre_name:
                            genre_names.append(genre_name)
                
                # Use first genre as primary, or "Film" if none
                primary_genre = genre_names[0] if genre_names else "Film"
                
                # Get poster URL
                poster_path = movie.get('poster_path', '')
                tvg_logo = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
                
                # Create vixsrc.to link
                movie_url = f"{self.vixsrc_base}/{tmdb_id}/?lang=it"
                
                # Create title with stars and genres
                display_title = f"{title} ({year})"
                
                # Write M3U entry with all metadata
                f.write(f'#EXTINF:-1 type="movie" tvg-logo="{tvg_logo}" group-title="Film - {primary_genre}",{display_title}\n')
                f.write(f"{movie_url}\n")
        
        print(f"Playlist generated successfully: {output_file}")
        print(f"Total movies: {len(movies_data)}")
    
    def create_popular_playlist(self, pages=5, output_file="tmdb_popular.m3u"):
        """Create playlist with popular movies"""
        all_movies = []
        
        for page in range(1, pages + 1):
            print(f"Fetching popular movies page {page}...")
            data = self.get_popular_movies(page=page)
            all_movies.extend(data['results'])
        
        self.generate_m3u_playlist(all_movies, output_file)
    
    def create_top_rated_playlist(self, pages=5, output_file="tmdb_top_rated.m3u"):
        """Create playlist with top rated movies"""
        all_movies = []
        
        for page in range(1, pages + 1):
            print(f"Fetching top rated movies page {page}...")
            data = self.get_top_rated_movies(page=page)
            all_movies.extend(data['results'])
        
        self.generate_m3u_playlist(all_movies, output_file)
    
    def create_complete_playlist(self):
        """Create one complete M3U file with all categories and genres"""
        print("Creating complete M3U playlist from vixsrc.to movies...")
        
        # Get genres mapping
        genres = self.get_movie_genres()
        
        # Fetch only movies that exist on vixsrc.to
        print(f"\nFetching movie details for {len(self.vixsrc_movies)} available movies...")
        movies_data = self._get_movies_from_vixsrc_list()
        
        # Count total movies that will be added
        total_movies = len(movies_data)
        
        output_path = os.path.join(self.output_dir, "film.m3u")
        with open(output_path, 'w', encoding='utf-8') as f:
            # Write M3U header with movie count
            f.write("#EXTM3U\n")
            f.write(f"#PLAYLIST:Film VixSrc ({total_movies} Film)\n\n")
            
            # Organize movies by categories
            self._organize_and_write_movies(f, movies_data, genres)

        # Save cache after completion
        self._save_cache()
        print(f"\nComplete playlist generated successfully: {output_path}")
        print(f"Cache updated with {len(self.cache)} total movies")
    
    def _get_movies_from_vixsrc_list(self):
        """Fetch movie details for all movies available on vixsrc.to, using cache when possible"""
        movies_data = []
        total_movies = len(self.vixsrc_movies)
        
        print(f"Fetching details for {total_movies} movies from TMDB (using cache)...")
        
        # Prepare list of tmdb_ids to fetch (not in cache)
        to_fetch = []
        for tmdb_id in self.vixsrc_movies:
            if str(tmdb_id) in self.cache:
                # Use cached data
                movies_data.append(self.cache[str(tmdb_id)])
            else:
                to_fetch.append(tmdb_id)
        
        print(f"{len(movies_data)} movies loaded from cache, {len(to_fetch)} to fetch from TMDB...")
        
        # Use ThreadPoolExecutor to fetch movie details in parallel
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_tmdb_id = {
                executor.submit(self._fetch_movie_details, tmdb_id): tmdb_id 
                for tmdb_id in to_fetch
            }
            completed = 0
            for future in as_completed(future_to_tmdb_id):
                tmdb_id = future_to_tmdb_id[future]
                try:
                    movie_data = future.result()
                    if movie_data:
                        movies_data.append(movie_data)
                        # Add to cache
                        if not self._is_movie_cached(movie_data):
                            self._add_to_cache(movie_data)
                    completed += 1
                    if completed % 100 == 0:
                        print(f"   Completed {completed}/{len(to_fetch)} TMDB requests...")
                except Exception as e:
                    print(f"   Error fetching movie {tmdb_id}: {e}")
        
        print(f"Successfully loaded {len(movies_data)} movie details (cache+TMDB)")
        return movies_data
    
    def _fetch_movie_details(self, tmdb_id):
        """Fetch movie details from TMDB by ID"""
        url = f"{self.base_url}/movie/{tmdb_id}"
        params = {
            'api_key': self.api_key,
            'language': 'it-IT'
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            movie_data = response.json()
            
            # Convert to the format expected by the rest of the code
            return {
                'id': movie_data['id'],
                'title': movie_data['title'],
                'release_date': movie_data.get('release_date', ''),
                'vote_average': movie_data.get('vote_average', 0),
                'poster_path': movie_data.get('poster_path', ''),
                'genre_ids': [genre['id'] for genre in movie_data.get('genres', [])]
            }
        except Exception as e:
            print(f"      Error fetching movie {tmdb_id}: {e}")
            return None
    
    def _organize_and_write_movies(self, file, movies_data, genres):
        """Organize movies by categories and write to file"""
        # Get real category data from TMDB
        print("Fetching real category data from TMDB...")
        
        # Get popular movies (real data)
        popular_ids = set()
        for page in range(1, 4):  # 3 pages for popular
            try:
                popular_data = self.get_popular_movies(page=page)
                for movie in popular_data['results']:
                    popular_ids.add(str(movie['id']))
            except Exception as e:
                print(f"Error fetching popular movies page {page}: {e}")
        
        # Get now playing movies (real data)
        cinema_ids = set()
        for page in range(1, 3):  # 2 pages for now playing
            try:
                cinema_data = self.get_latest_movies(page=page)
                for movie in cinema_data['results']:
                    cinema_ids.add(str(movie['id']))
            except Exception as e:
                print(f"Error fetching cinema movies page {page}: {e}")
        
        # Get top rated movies (real data)
        latest_ids = set()
        for page in range(1, 3):  # 2 pages for top rated
            try:
                latest_data = self.get_top_rated_movies(page=page)
                for movie in latest_data['results']:
                    latest_ids.add(str(movie['id']))
            except Exception as e:
                print(f"Error fetching top rated movies page {page}: {e}")
        
        # Group movies by real categories
        cinema_movies = []
        popular_movies = []
        latest_movies = []
        genre_movies = {genre_name: [] for genre_name in genres.values()}
        
        # Process all movies
        for movie in movies_data:
            movie_id = str(movie['id'])
            
            # Add to appropriate categories based on real TMDB data
            if movie_id in cinema_ids:
                cinema_movies.append(movie)
            if movie_id in popular_ids:
                popular_movies.append(movie)
            if movie_id in latest_ids:
                latest_movies.append(movie)
            
            # Add to genre categories
            for genre_id in movie['genre_ids']:
                genre_name = genres.get(genre_id)
                if genre_name:
                    genre_movies[genre_name].append(movie)
        
        # Write sections
        # 1. Film Al Cinema (limit 50)
        print("\n1. Adding 'Film Al Cinema' section...")
        file.write("# Al Cinema\n")
        added_count = 0
        for movie in cinema_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Al Cinema"):
                added_count += 1
        print(f"   Added {added_count} movies to Al Cinema")
        
        # 2. Popolari (limit 50)
        print("\n2. Adding 'Popolari' section...")
        file.write("\n# Popolari\n")
        added_count = 0
        for movie in popular_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Popolari"):
                added_count += 1
        print(f"   Added {added_count} movies to Popolari")
        
        # 3. Più Votati (limit 50)
        print("\n3. Adding 'Più Votati' section...")
        file.write("\n# Più Votati\n")
        added_count = 0
        for movie in latest_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Più Votati"):
                added_count += 1
        print(f"   Added {added_count} movies to Più Votati")
        
        # 4. Genres
        print("\n4. Adding genre-specific sections...")
        for genre_name, movies in genre_movies.items():
            if movies:  # Only add genres that have movies
                print(f"   Adding '{genre_name}' section ({len(movies)} movies)...")
                file.write(f"\n# {genre_name}\n")
                # Ordina i film dal più nuovo al più vecchio
                movies_sorted = sorted(
                    movies,
                    key=lambda m: m.get('release_date', ''),
                    reverse=True
                )
                added_count = 0
                for movie in movies_sorted:
                    if self._write_movie_entry(file, movie, genres, genre_name):
                        added_count += 1
                print(f"      Added {added_count} movies to {genre_name}")
    
    def _create_playlist_from_cache(self, file, genres):
        """Create playlist using only cached movies"""
        print(f"Creating playlist from {len(self.cache)} cached movies...")
        
        # Group movies by categories
        cinema_movies = []
        popular_movies = []
        latest_movies = []
        genre_movies = {genre_name: [] for genre_name in genres.values()}
        
        # Process all cached movies
        for movie_data in self.cache.values():
            movie = {
                'id': movie_data['id'],
                'title': movie_data['title'],
                'release_date': movie_data['release_date'],
                'vote_average': movie_data['vote_average'],
                'poster_path': movie_data['poster_path'],
                'genre_ids': movie_data['genre_ids']
            }
            
            # Add to appropriate categories based on genres and rating
            if movie_data['vote_average'] >= 7.5:
                latest_movies.append(movie)
            elif movie_data['vote_average'] >= 6.5:
                popular_movies.append(movie)
            else:
                cinema_movies.append(movie)
            
            # Add to genre categories
            for genre_id in movie_data['genre_ids']:
                genre_name = genres.get(genre_id)
                if genre_name:
                    genre_movies[genre_name].append(movie)
        
        # Write sections
        # 1. Film Al Cinema (limit 50)
        print("\n1. Adding 'Film Al Cinema' section...")
        file.write("# Al Cinema\n")
        added_count = 0
        for movie in cinema_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Al Cinema"):
                added_count += 1
        print(f"   Added {added_count} movies to Al Cinema")
        
        # 2. Popolari (limit 50)
        print("\n2. Adding 'Popolari' section...")
        file.write("\n# Popolari\n")
        added_count = 0
        for movie in popular_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Popolari"):
                added_count += 1
        print(f"   Added {added_count} movies to Popolari")
        
        # 3. Più Votati (limit 50)
        print("\n3. Adding 'Più Votati' section...")
        file.write("\n# Più Votati\n")
        added_count = 0
        for movie in latest_movies[:50]:
            if self._write_movie_entry(file, movie, genres, "Più Votati"):
                added_count += 1
        print(f"   Added {added_count} movies to Più Votati")
        
        # 4. Genres
        print("\n4. Adding genre-specific sections...")
        for genre_name, movies in genre_movies.items():
            if movies:  # Only add genres that have movies
                print(f"   Adding '{genre_name}' section ({len(movies)} movies)...")
                file.write(f"\n# {genre_name}\n")
                # Ordina i film dal più nuovo al più vecchio
                movies_sorted = sorted(
                    movies,
                    key=lambda m: m.get('release_date', ''),
                    reverse=True
                )
                added_count = 0
                for movie in movies_sorted:
                    if self._write_movie_entry(file, movie, genres, genre_name):
                        added_count += 1
                print(f"      Added {added_count} movies to {genre_name}")
    
    def _get_all_movies_by_endpoint(self, endpoint, max_pages=500, limit=None):
        """Get all movies from a specific endpoint using multithreading and cache"""
        print(f"   Fetching {endpoint} movies (max {max_pages} pages, limit: {limit})...")
        
        # First, get the total number of pages
        first_response = requests.get(f"{self.base_url}/movie/{endpoint}", params={
            'api_key': self.api_key,
            'page': 1,
            'language': 'it-IT'
        })
        first_response.raise_for_status()
        first_data = first_response.json()
        total_pages = min(first_data['total_pages'], max_pages)
        
        print(f"   Total pages to fetch: {total_pages}")
        
        # Use ThreadPoolExecutor to fetch pages in parallel
        all_movies = []
        new_movies_count = 0
        cached_movies_count = 0
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit all page requests
            future_to_page = {
                executor.submit(self._fetch_page, endpoint, page): page 
                for page in range(1, total_pages + 1)
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    movies = future.result()
                    
                    # Check cache for each movie
                    for movie in movies:
                        if self._is_movie_cached(movie):
                            cached_movies_count += 1
                        else:
                            self._add_to_cache(movie)
                            new_movies_count += 1
                    
                    all_movies.extend(movies)
                    completed += 1
                    if completed % 10 == 0:
                        print(f"   Completed {completed}/{total_pages} pages... (New: {new_movies_count}, Cached: {cached_movies_count})")
                except Exception as e:
                    print(f"   Error fetching page {page}: {e}")
        
        # Apply limit if specified
        if limit and len(all_movies) > limit:
            all_movies = all_movies[:limit]
            print(f"   Limited to {limit} movies")
        
        print(f"   Total {endpoint} movies: {len(all_movies)} (New: {new_movies_count}, Cached: {cached_movies_count})")
        return all_movies
    
    def _fetch_page(self, endpoint, page):
        """Fetch a single page of movies with optimized settings"""
        url = f"{self.base_url}/movie/{endpoint}"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': 'it-IT'
        }
        
        # Optimized request settings
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'TMDB-M3U-Generator/1.0',
            'Accept': 'application/json'
        })
        
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return data['results']
    
    def _get_all_movies_by_genre(self, genre_id, max_pages=500):
        """Get all movies for a specific genre using multithreading and cache"""
        # First, get the total number of pages
        first_response = requests.get(f"{self.base_url}/discover/movie", params={
            'api_key': self.api_key,
            'page': 1,
            'language': 'it-IT',
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'include_video': False,
            'with_genres': genre_id
        })
        first_response.raise_for_status()
        first_data = first_response.json()
        total_pages = min(first_data['total_pages'], max_pages)
        
        # Use ThreadPoolExecutor to fetch pages in parallel
        all_movies = []
        new_movies_count = 0
        cached_movies_count = 0
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            # Submit all page requests
            future_to_page = {
                executor.submit(self._fetch_genre_page, genre_id, page): page 
                for page in range(1, total_pages + 1)
            }
            
            # Collect results as they complete
            completed = 0
            for future in as_completed(future_to_page):
                page = future_to_page[future]
                try:
                    movies = future.result()
                    
                    # Check cache for each movie
                    for movie in movies:
                        if self._is_movie_cached(movie):
                            cached_movies_count += 1
                        else:
                            self._add_to_cache(movie)
                            new_movies_count += 1
                    
                    all_movies.extend(movies)
                    completed += 1
                    if completed % 10 == 0:
                        print(f"      Completed {completed}/{total_pages} pages... (New: {new_movies_count}, Cached: {cached_movies_count})")
                except Exception as e:
                    print(f"      Error fetching genre page {page}: {e}")
        
        print(f"      Total genre movies: {len(all_movies)} (New: {new_movies_count}, Cached: {cached_movies_count})")
        return all_movies
    
    def _fetch_genre_page(self, genre_id, page):
        """Fetch a single page of movies for a specific genre with optimized settings"""
        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'page': page,
            'language': 'it-IT',
            'sort_by': 'popularity.desc',
            'include_adult': False,
            'include_video': False,
            'with_genres': genre_id
        }
        
        # Optimized request settings
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'TMDB-M3U-Generator/1.0',
            'Accept': 'application/json'
        })
        
        response = session.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        return data['results']
    
    def _write_movie_entry(self, file, movie, genres, group_title):
        """Write a single movie entry to the M3U file"""
        tmdb_id = movie['id']
        
        # Check if movie is available on vixsrc.to
        if not self._is_movie_available_on_vixsrc(tmdb_id):
            return False  # Skip this movie
        
        title = movie['title']
        year = movie.get('release_date', '')[:4] if movie.get('release_date') else ''
        
        # Get rating and create stars
        rating = movie.get('vote_average', 0)
        stars = "★" * int(rating / 2) + "☆" * (5 - int(rating / 2)) if rating > 0 else "☆☆☆☆☆"
        
        # Get all genres
        genre_names = []
        if movie.get('genre_ids') and movie['genre_ids']:
            for genre_id in movie['genre_ids']:
                genre_name = genres.get(genre_id, "")
                if genre_name:
                    genre_names.append(genre_name)
        
        # Get poster URL
        poster_path = movie.get('poster_path', '')
        tvg_logo = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else ""
        
        # Create vixsrc.to link
        movie_url = f"{self.vixsrc_base}/{tmdb_id}/?lang=it"
        
        # Create title with stars and genres
        display_title = f"{title} ({year})"
        
        # Write M3U entry
        file.write(f'#EXTINF:-1 tvg-logo="{tvg_logo}" group-title="Film - {group_title}",{display_title}\n')
        file.write(f"{movie_url}\n\n")
        return True  # Movie was added
    

    
    def create_all_movies_playlist(self, pages=50, output_file="tmdb_movies.m3u"):
        """Create playlist with all available movies"""
        all_movies = []
        
        for page in range(1, pages + 1):
            print(f"Fetching all movies page {page}...")
            data = self.get_all_movies(page=page)
            all_movies.extend(data['results'])
            
            # Check if we've reached the end
            if page >= data['total_pages']:
                break
        
        self.generate_m3u_playlist(all_movies, output_file)
    
    def create_latest_playlist(self, pages=3, output_file="tmdb_latest.m3u"):
        """Create playlist with latest movies"""
        all_movies = []
        
        for page in range(1, pages + 1):
            print(f"Fetching latest movies page {page}...")
            data = self.get_latest_movies(page=page)
            all_movies.extend(data['results'])
        
        self.generate_m3u_playlist(all_movies, output_file)

def main():
    """Main function to run the generator"""
    try:
        generator = TMDBM3UGenerator()
        
        print("TMDB M3U Playlist Generator")
        print("=" * 40)
        
        # Create complete playlist
        generator.create_complete_playlist()
        
        print("\nAll playlists generated successfully!")
        

        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your TMDB_API_KEY environment variable:")
        print("1. Get your API key from https://www.themoviedb.org/settings/api")
        print("2. Create a .env file with: TMDB_API_KEY=your_api_key_here")

if __name__ == "__main__":
    main() 