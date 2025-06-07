import requests
import time
import os
from typing import List, Dict, Optional, Tuple, Any


class GitHubAPI:
    """
    Class to handle all GitHub API interactions with proper rate limit handling and pagination
    """
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize with optional GitHub token for authentication
        
        Args:
            token: GitHub personal access token
        """
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        
        if token:
            self.headers["Authorization"] = f"token {token}"
            
        # Track rate limits
        self.rate_limit = 0
        self.rate_limit_remaining = 0
        self.rate_limit_reset = 0
        
    def _make_request(self, url: str) -> Tuple[bool, Any]:
        """
        Make a request to the GitHub API with proper error handling
        
        Args:
            url: The URL to request
            
        Returns:
            Tuple of (success, data)
        """
        try:
            response = requests.get(url, headers=self.headers)
            
            # Update rate limit info
            if 'X-RateLimit-Limit' in response.headers:
                self.rate_limit = int(response.headers['X-RateLimit-Limit'])
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
                self.rate_limit_reset = int(response.headers['X-RateLimit-Reset'])
            
            # Check if we're close to rate limit
            if self.rate_limit_remaining < 5:
                reset_time = self.rate_limit_reset - time.time()
                if reset_time > 0:
                    print(f"Warning: Rate limit almost reached. Waiting for {int(reset_time)} seconds...")
                    time.sleep(reset_time + 1)
            
            if response.status_code == 200:
                return True, response.json()
            elif response.status_code == 404:
                return False, {"error": "User not found"}
            elif response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers and response.headers['X-RateLimit-Remaining'] == '0':
                reset_time = int(response.headers['X-RateLimit-Reset']) - time.time()
                return False, {"error": f"Rate limit exceeded. Resets in {int(reset_time)} seconds."}
            else:
                return False, {"error": f"API request failed with status code {response.status_code}: {response.text}"}
                
        except requests.exceptions.ConnectionError:
            return False, {"error": "Connection error. Please check your internet connection."}
        except requests.exceptions.Timeout:
            return False, {"error": "Request timed out. GitHub might be experiencing issues."}
        except requests.exceptions.RequestException as e:
            return False, {"error": f"Request error: {str(e)}"}
        except Exception as e:
            return False, {"error": f"Unexpected error: {str(e)}"}
    
    def get_user_info(self, username: str) -> Tuple[bool, Dict]:
        """
        Get information about a GitHub user
        
        Args:
            username: GitHub username
            
        Returns:
            Tuple of (success, user_data)
        """
        url = f"{self.BASE_URL}/users/{username}"
        return self._make_request(url)
    
    def get_all_followers(self, username: str) -> Tuple[bool, List[Dict]]:
        """
        Get all followers for a user with pagination
        
        Args:
            username: GitHub username
            
        Returns:
            Tuple of (success, followers_list)
        """
        followers = []
        page = 1
        per_page = 100  # Maximum allowed by GitHub API
        
        while True:
            url = f"{self.BASE_URL}/users/{username}/followers?page={page}&per_page={per_page}"
            success, data = self._make_request(url)
            
            if not success:
                return False, data
            
            if not data:  # Empty page means we've got all followers
                break
                
            followers.extend(data)
            page += 1
            
            # If we didn't get a full page, we've reached the end
            if len(data) < per_page:
                break
        
        return True, followers
    
    def get_all_following(self, username: str) -> Tuple[bool, List[Dict]]:
        """
        Get all users that a user is following with pagination
        
        Args:
            username: GitHub username
            
        Returns:
            Tuple of (success, following_list)
        """
        following = []
        page = 1
        per_page = 100  # Maximum allowed by GitHub API
        
        while True:
            url = f"{self.BASE_URL}/users/{username}/following?page={page}&per_page={per_page}"
            success, data = self._make_request(url)
            
            if not success:
                return False, data
            
            if not data:  # Empty page means we've got all following
                break
                
            following.extend(data)
            page += 1
            
            # If we didn't get a full page, we've reached the end
            if len(data) < per_page:
                break
        
        return True, following
    
    def get_rate_limit_info(self) -> Dict:
        """
        Get information about the current rate limit status
        
        Returns:
            Dictionary with rate limit information
        """
        return {
            "limit": self.rate_limit,
            "remaining": self.rate_limit_remaining,
            "reset_time": self.rate_limit_reset
        } 