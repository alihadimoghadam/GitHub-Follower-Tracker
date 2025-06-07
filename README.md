# GitHub Follower Tracker

A powerful command-line tool to analyze GitHub follow relationships. Track who's not following you back, who you're not following back, and get detailed statistics about your GitHub social network.

## Features

- **Complete API Coverage**: Retrieves all followers and following with pagination support
- **GitHub Token Support**: Optional authentication to increase API rate limits from 60 to 5000 requests/hour
- **Caching**: Reduce API calls by caching results locally
- **Comprehensive Analysis**:
  - Users not following you back
  - Followers you're not following back
  - Mutual followers
  - Detailed statistics and metrics
- **Data Export**: Export results to CSV or JSON formats
- **Error Handling**: Robust error handling and rate limit management

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/alihadimoghadam/GitHub-Follower-Tracker.git
   cd GitHub-Follower-Tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Basic usage:

```
python main.py USERNAME
```

Replace `USERNAME` with your GitHub username or any GitHub user you want to analyze.

### Command-line Options

```
python main.py USERNAME [OPTIONS]
```

Options:
- `--token`, `-t`: GitHub API token (increases rate limits from 60 to 5000 requests/hour)
- `--no-cache`: Disable caching of API responses
- `--clear-cache`: Clear existing cached data before running
- `--max-display N`: Maximum number of users to display in lists (default: 10)
- `--export-dir DIR`: Directory for exported files (default: "exports")
- `--export-format FORMAT`: Export format for user lists (csv or json, default: csv)
- `--export-all`: Export all data (followers, following, mutual followers)

### Using a GitHub Token

For better performance and higher rate limits, you can provide a GitHub token in three ways:

1. Command-line option: `python main.py USERNAME --token YOUR_TOKEN`
2. Environment variable: `export GITHUB_TOKEN=YOUR_TOKEN`
3. Interactive prompt: The program will ask if you want to provide a token

To create a GitHub token:
1. Go to GitHub Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. Click "Generate new token"
3. Give it a name and select the "public_repo" scope
4. Click "Generate token" and copy the token

## Example Output

```
===============================================================
 GITHUB FOLLOWER ANALYSIS FOR: octocat (The Octocat)
===============================================================

Account Stats:
  Followers:     10000
  Following:     100
  Follow Ratio:  100.00 (followers/following)
  Join Date:     2011-01-25T18:44:36Z
  Account Age:   4800 days
  Public Repos:  8

Follow Analysis:
  Mutual Follows:          50 (50.0%)
  Not Following You Back:  50 (50.0%)
  You're Not Following:    9950 (99.5%)

Summary exported to: exports/octocat_summary.json

----------------------------------------
 USERS NOT FOLLOWING YOU BACK (50 users)
----------------------------------------
  1. user1 (https://github.com/user1)
  2. user2 (https://github.com/user2)
  3. user3 (https://github.com/user3)
  ...

  ... and 40 more not shown

Exported to: exports/octocat_not_following_back.csv

----------------------------------------
 FOLLOWERS YOU'RE NOT FOLLOWING BACK (9950 users)
----------------------------------------
  1. user10 (https://github.com/user10)
  2. user11 (https://github.com/user11)
  3. user12 (https://github.com/user12)
  ...

  ... and 9940 more not shown

Exported to: exports/octocat_not_following.csv

Analysis complete!
```

## Exported Files

The program automatically exports the analysis results to the "exports" directory (or the directory specified with `--export-dir`):

- `USERNAME_summary.json`: Summary of the analysis
- `USERNAME_not_following_back.csv`: Users not following you back
- `USERNAME_not_following.csv`: Followers you're not following back

With the `--export-all` option, it also exports:
- `USERNAME_mutual_followers.csv`: Users with mutual follow relationship
- `USERNAME_all_followers.csv`: All followers
- `USERNAME_all_following.csv`: All users being followed

## Limitations

- The GitHub API has rate limits (60 requests/hour without authentication, 5000 requests/hour with a token)
- For users with a large number of followers/following, the analysis may take longer to complete
- The tool requires internet access to fetch data from GitHub

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

The program is built using the following libraries:

- [Tkinter](https://docs.python.org/3/library/tkinter.html): Python's standard GUI package.
- [requests](https://pypi.org/project/requests/): A Python library for making HTTP requests.

## Contributing

Contributions to the project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

---

Feel free to update and customize the README file according to your project's specific details and requirements.
