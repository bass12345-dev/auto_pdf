import requests
import os
import json
import time
import re
from src.credentials.cred import notion_headers,bucket_name

# Cache directory
CACHE_DIR = "./notion_cache"
cache_duration = 86400
# Ensure the cache directory exists
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def sanitize_filename(query_key):
    """Sanitize the query key to create a valid filename."""
    # Remove characters that are not allowed in filenames (e.g., slashes, quotes, etc.)
    sanitized_key = re.sub(r'[<>:"/\\|?*]', '_', query_key)
    return sanitized_key

def get_cache_file_path(query_key):
    """Generate a file path for the cache based on the query key."""
    sanitized_key = sanitize_filename(query_key.replace(" ", "_"))
    return os.path.join(CACHE_DIR, f"{sanitized_key}.json")

def save_to_cache(query_key, data):
    """Save the API response to a JSON file in the cache directory."""
    cache_file = get_cache_file_path(query_key)
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def load_from_cache(query_key, cache_duration):
    """Load cached data if available and not expired."""
    cache_file = get_cache_file_path(query_key)
    if os.path.exists(cache_file):
        # Check file's modified time
        file_mod_time = os.path.getmtime(cache_file)
        t = time.time() - file_mod_time
        print(t)
        if time.time() - file_mod_time < cache_duration:
            with open(cache_file, 'r') as f:
                return json.load(f)
        else:
            try:
                if os.path.exists(cache_file):
                    os.remove(cache_file)
                    print(f"Cache file '{cache_file}' deleted.")
                else:
                    print("Cache file does not exist.")
            except OSError as e:
                print(f"Error deleting cache file: {e}")
            print("Cache expired. Making a new API request.")
    return None



def get_notion_data(api_url, query):
    """
    Get data from the Notion API and cache responses to a folder.
    
    Args:
    - api_url: The Notion API endpoint URL.
    - query: The query to send to the API.
    - cache_duration: Cache expiration time in seconds.
    
    Returns:
    - API response (or cached result).
    """
    # Convert the query to a string to generate a unique cache key
    query_key = json.dumps(query, sort_keys=True)

    # Load from cache if available
    cached_data = load_from_cache(query_key, cache_duration)
    if cached_data is not None:
        print("Returning cached result")
        return cached_data

    # If no cached data, make the API request
    print("Making API request to Notion")
    url = f"https://api.notion.com/v1/blocks/{api_url}/children"
    response = requests.get(url, headers=notion_headers)

    if response.status_code == 200:
        data = response.json()

        # If no results, save an empty result to cache
        if not data.get("results"):
            save_to_cache(query_key, {"results": []})
            print("No results found, caching this empty result.")
            return None

        # Save the successful response to cache
        save_to_cache(query_key, data)
        return data
    else:
        print(f"API request failed with status code {response.status_code}")
        return {"results": []}



# Set the cache duration to 1 month (2592000 seconds)
 # 1 month in seconds

