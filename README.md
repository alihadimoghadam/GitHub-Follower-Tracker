# GitHub Follower Analyzer

GitHub Follower Analyzer is a Python program that allows you to analyze your GitHub followers and identify users who are not following you back. It utilizes the GitHub API to retrieve follower and following data.

## Prerequisites

Before running the program, make sure you have the following installed:

- Python 3: The code is written in Python 3, so ensure you have Python 3 installed on your system.

## Installation

1. Clone the repository or download the code files.
2. Install the required Python packages by running the following command:
   ```
   pip install requests
   ```
3. Run the program using the following command:
   ```
   python github_follower_analyzer.py
   ```

## Usage

1. Enter your GitHub username in the provided text field.
2. Click the "Find Users" button to initiate the search.
3. The program will retrieve your followers and following data from GitHub.
4. The results will be displayed in the text box, showing the users who are not following you back.

## Dependencies

The program relies on the following Python packages:

- `requests`: Used to send HTTP requests to the GitHub API and retrieve follower and following data.

## Limitations

- The program relies on the GitHub API to retrieve follower and following data. Ensure you have a stable internet connection and your GitHub API rate limit is not exceeded.
- Large numbers of followers or following may result in longer response times.
- The program currently displays the results within the GUI. If you want to export the results to a file or perform additional actions, you may need to modify the code accordingly.

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