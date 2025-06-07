from typing import Dict, List, Tuple, Any
import datetime

class FollowerAnalytics:
    """
    Analyze GitHub follower relationships and provide insights
    """
    
    def __init__(self, user_data: Dict, followers: List[Dict], following: List[Dict]):
        """
        Initialize with user data and relationships
        
        Args:
            user_data: GitHub user data
            followers: List of user's followers
            following: List of users being followed
        """
        self.user_data = user_data
        self.followers = followers
        self.following = following
        
        # Extract login names for easier comparison
        self.follower_logins = {f["login"] for f in followers}
        self.following_logins = {f["login"] for f in following}
        
    def get_not_following_back(self) -> List[Dict]:
        """
        Get users who are not following the user back
        
        Returns:
            List of users not following back
        """
        not_following_back_logins = self.following_logins - self.follower_logins
        return [user for user in self.following if user["login"] in not_following_back_logins]
    
    def get_not_following(self) -> List[Dict]:
        """
        Get followers who the user is not following back
        
        Returns:
            List of users not being followed back
        """
        not_following_logins = self.follower_logins - self.following_logins
        return [user for user in self.followers if user["login"] in not_following_logins]
    
    def get_mutual_followers(self) -> List[Dict]:
        """
        Get users with mutual follow relationship
        
        Returns:
            List of mutual followers
        """
        mutual_logins = self.follower_logins.intersection(self.following_logins)
        return [user for user in self.followers if user["login"] in mutual_logins]
    
    def generate_summary(self) -> Dict:
        """
        Generate a summary of follow relationships
        
        Returns:
            Dictionary with summary statistics
        """
        not_following_back = self.get_not_following_back()
        not_following = self.get_not_following()
        mutual = self.get_mutual_followers()
        
        # Calculate percentages
        total_following = len(self.following)
        total_followers = len(self.followers)
        
        if total_following > 0:
            percent_not_following_back = (len(not_following_back) / total_following) * 100
        else:
            percent_not_following_back = 0
            
        if total_followers > 0:
            percent_not_following = (len(not_following) / total_followers) * 100
        else:
            percent_not_following = 0
            
        mutual_percentage = 0
        if total_following > 0 and total_followers > 0:
            mutual_percentage = (len(mutual) / max(total_following, total_followers)) * 100
        
        # Calculate follow ratio
        follow_ratio = 0
        if total_following > 0:
            follow_ratio = total_followers / total_following
            
        # Get join date in ISO format
        join_date = None
        if "created_at" in self.user_data:
            join_date = self.user_data["created_at"]
            
        # Calculate account age in days
        account_age_days = 0
        if join_date:
            try:
                created_date = datetime.datetime.strptime(join_date, "%Y-%m-%dT%H:%M:%SZ")
                account_age_days = (datetime.datetime.now() - created_date).days
            except (ValueError, TypeError):
                pass
            
        return {
            "username": self.user_data.get("login", "Unknown"),
            "name": self.user_data.get("name", "Unknown"),
            "total_followers": total_followers,
            "total_following": total_following,
            "not_following_back_count": len(not_following_back),
            "not_following_count": len(not_following),
            "mutual_count": len(mutual),
            "percent_not_following_back": round(percent_not_following_back, 2),
            "percent_not_following": round(percent_not_following, 2),
            "mutual_percentage": round(mutual_percentage, 2),
            "follow_ratio": round(follow_ratio, 2),
            "join_date": join_date,
            "account_age_days": account_age_days,
            "public_repos": self.user_data.get("public_repos", 0),
            "public_gists": self.user_data.get("public_gists", 0)
        } 