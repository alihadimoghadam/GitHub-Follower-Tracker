#!/usr/bin/env python3
import os
import sys
import argparse
import getpass
from typing import List, Dict, Optional, Any

from github_api import GitHubAPI
from cache import Cache
from analytics import FollowerAnalytics
from exporter import DataExporter

def print_header(text: str) -> None:
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def print_section(text: str) -> None:
    """Print a formatted section header"""
    print("\n" + "-" * 40)
    print(f" {text}")
    print("-" * 40)

def print_user_list(users: List[Dict], max_display: int = 10) -> None:
    """
    Print a list of GitHub users
    
    Args:
        users: List of user dictionaries
        max_display: Maximum number of users to display
    """
    if not users:
        print("  None")
        return
        
    # Determine if we need to truncate the list
    truncated = len(users) > max_display
    display_users = users[:max_display]
    
    # Display users
    for i, user in enumerate(display_users, 1):
        print(f"  {i}. {user['login']} ({user.get('html_url', '')})")
    
    # Show truncation message if needed
    if truncated:
        print(f"\n  ... and {len(users) - max_display} more not shown")

def print_summary(summary: Dict) -> None:
    """
    Print a formatted summary of the analysis
    
    Args:
        summary: Dictionary with analysis summary
    """
    print_header(f"GITHUB FOLLOWER ANALYSIS FOR: {summary['username']} ({summary['name']})")
    
    print(f"\nAccount Stats:")
    print(f"  Followers:     {summary['total_followers']}")
    print(f"  Following:     {summary['total_following']}")
    print(f"  Follow Ratio:  {summary['follow_ratio']:.2f} (followers/following)")
    print(f"  Join Date:     {summary['join_date']}")
    print(f"  Account Age:   {summary['account_age_days']} days")
    print(f"  Public Repos:  {summary['public_repos']}")
    
    print(f"\nFollow Analysis:")
    print(f"  Mutual Follows:          {summary['mutual_count']} ({summary['mutual_percentage']:.1f}%)")
    print(f"  Not Following You Back:  {summary['not_following_back_count']} ({summary['percent_not_following_back']:.1f}%)")
    print(f"  You're Not Following:    {summary['not_following_count']} ({summary['percent_not_following']:.1f}%)")

def run_analysis(username: str, token: Optional[str] = None, use_cache: bool = True, cache_max_age: int = 3600) -> Dict:
    """
    Run the GitHub follower analysis
    
    Args:
        username: GitHub username to analyze
        token: GitHub API token (optional)
        use_cache: Whether to use cached data
        cache_max_age: Maximum age of cached data in seconds
        
    Returns:
        Analysis results dictionary
    """
    # Set up API and cache
    api = GitHubAPI(token)
    cache = Cache(max_age=cache_max_age) if use_cache else None
    
    # Get user info
    if use_cache:
        user_data = cache.get(f"user_info_{username}")
    else:
        user_data = None
        
    if not user_data:
        print(f"Fetching user data for {username}...")
        success, user_data = api.get_user_info(username)
        if not success:
            print(f"Error: {user_data.get('error', 'Unknown error')}")
            sys.exit(1)
        if use_cache:
            cache.set(f"user_info_{username}", user_data)
    
    # Get followers
    if use_cache:
        followers = cache.get(f"followers_{username}")
    else:
        followers = None
        
    if not followers:
        print(f"Fetching followers for {username}...")
        success, followers = api.get_all_followers(username)
        if not success:
            print(f"Error: {followers.get('error', 'Unknown error')}")
            sys.exit(1)
        if use_cache:
            cache.set(f"followers_{username}", followers)
    
    # Get following
    if use_cache:
        following = cache.get(f"following_{username}")
    else:
        following = None
        
    if not following:
        print(f"Fetching users {username} is following...")
        success, following = api.get_all_following(username)
        if not success:
            print(f"Error: {following.get('error', 'Unknown error')}")
            sys.exit(1)
        if use_cache:
            cache.set(f"following_{username}", following)
    
    # Create analytics object
    analytics = FollowerAnalytics(user_data, followers, following)
    
    # Generate and return results
    return {
        "user_data": user_data,
        "followers": followers,
        "following": following,
        "not_following_back": analytics.get_not_following_back(),
        "not_following": analytics.get_not_following(),
        "mutual_followers": analytics.get_mutual_followers(),
        "summary": analytics.generate_summary()
    }

def main():
    """Main entry point for the command-line application"""
    parser = argparse.ArgumentParser(
        description="GitHub Follower Tracker - Analyze your GitHub followers and following"
    )
    
    parser.add_argument("username", help="GitHub username to analyze")
    parser.add_argument("--token", "-t", help="GitHub API token (optional, increases rate limits)")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching of API responses")
    parser.add_argument("--clear-cache", action="store_true", help="Clear existing cached data before running")
    parser.add_argument("--max-display", type=int, default=10, help="Maximum number of users to display in lists")
    parser.add_argument("--export-dir", default="exports", help="Directory for exported files")
    parser.add_argument("--export-format", choices=["csv", "json"], default="csv", help="Export format for user lists")
    parser.add_argument("--export-all", action="store_true", help="Export all data")
    
    args = parser.parse_args()
    
    # Create cache instance
    cache = Cache()
    
    # Clear cache if requested
    if args.clear_cache:
        print("Clearing cache...")
        cache.clear()
    
    # Check for token in environment variable if not provided
    token = args.token
    if not token and "GITHUB_TOKEN" in os.environ:
        token = os.environ["GITHUB_TOKEN"]
        
    # If still no token, check if user wants to provide one
    if not token:
        print("No GitHub API token found. Using a token increases rate limits (5000 vs 60 requests/hour).")
        use_token = input("Would you like to provide a token? (y/n): ").lower() == 'y'
        if use_token:
            token = getpass.getpass("Enter your GitHub token: ")
    
    # Run the analysis
    print(f"Analyzing GitHub user: {args.username}")
    results = run_analysis(
        args.username,
        token=token,
        use_cache=not args.no_cache
    )
    
    # Create export directory if needed
    os.makedirs(args.export_dir, exist_ok=True)
    
    # Print and export results
    summary = results["summary"]
    print_summary(summary)
    
    # Export summary
    summary_path = os.path.join(args.export_dir, f"{args.username}_summary.json")
    DataExporter.export_summary(summary, summary_path)
    print(f"\nSummary exported to: {summary_path}")
    
    # Not following back
    not_following_back = results["not_following_back"]
    print_section(f"USERS NOT FOLLOWING YOU BACK ({len(not_following_back)} users)")
    print_user_list(not_following_back, args.max_display)
    
    # Export not following back
    not_following_back_path = os.path.join(args.export_dir, f"{args.username}_not_following_back.{args.export_format}")
    DataExporter.export_user_list(not_following_back, not_following_back_path, args.export_format)
    print(f"\nExported to: {not_following_back_path}")
    
    # Not following
    not_following = results["not_following"]
    print_section(f"FOLLOWERS YOU'RE NOT FOLLOWING BACK ({len(not_following)} users)")
    print_user_list(not_following, args.max_display)
    
    # Export not following
    not_following_path = os.path.join(args.export_dir, f"{args.username}_not_following.{args.export_format}")
    DataExporter.export_user_list(not_following, not_following_path, args.export_format)
    print(f"\nExported to: {not_following_path}")
    
    # Export all data if requested
    if args.export_all:
        # Export mutual followers
        mutual_path = os.path.join(args.export_dir, f"{args.username}_mutual_followers.{args.export_format}")
        DataExporter.export_user_list(results["mutual_followers"], mutual_path, args.export_format)
        print(f"Exported mutual followers to: {mutual_path}")
        
        # Export all followers
        followers_path = os.path.join(args.export_dir, f"{args.username}_all_followers.{args.export_format}")
        DataExporter.export_user_list(results["followers"], followers_path, args.export_format)
        print(f"Exported all followers to: {followers_path}")
        
        # Export all following
        following_path = os.path.join(args.export_dir, f"{args.username}_all_following.{args.export_format}")
        DataExporter.export_user_list(results["following"], following_path, args.export_format)
        print(f"Exported all following to: {following_path}")
    
    print("\nAnalysis complete!")
    
if __name__ == "__main__":
    main() 