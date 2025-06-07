import json
import os
import time
from typing import Dict, List, Any, Optional

class Cache:
    """
    Simple caching system to store GitHub API results to reduce API calls
    """
    
    def __init__(self, cache_dir: str = ".cache", max_age: int = 3600):
        """
        Initialize the cache
        
        Args:
            cache_dir: Directory to store cache files
            max_age: Maximum age of cache entries in seconds (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.max_age = max_age
        
        # Create cache directory if it doesn't exist
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def _get_cache_path(self, key: str) -> str:
        """
        Get the filesystem path for a cache key
        
        Args:
            key: Cache key
            
        Returns:
            Path to the cache file
        """
        # Ensure the key is filesystem safe
        safe_key = "".join(c if c.isalnum() else "_" for c in key)
        return os.path.join(self.cache_dir, f"{safe_key}.json")
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is expired
            if time.time() - cache_data["timestamp"] > self.max_age:
                return None
                
            return cache_data["data"]
        except (json.JSONDecodeError, KeyError, IOError):
            # If there's any error reading the cache, return None
            return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Store a value in the cache
        
        Args:
            key: Cache key
            value: Value to cache
        """
        cache_path = self._get_cache_path(key)
        
        cache_data = {
            "timestamp": time.time(),
            "data": value
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
        except IOError as e:
            print(f"Warning: Failed to write cache file {cache_path}: {str(e)}")
    
    def clear(self, key: Optional[str] = None) -> None:
        """
        Clear cache entries
        
        Args:
            key: Specific key to clear, or None to clear all
        """
        if key:
            cache_path = self._get_cache_path(key)
            if os.path.exists(cache_path):
                try:
                    os.remove(cache_path)
                except IOError as e:
                    print(f"Warning: Failed to remove cache file {cache_path}: {str(e)}")
        else:
            # Clear all cache files
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.json'):
                    try:
                        os.remove(os.path.join(self.cache_dir, filename))
                    except IOError:
                        pass 