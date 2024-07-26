# Take Home Project

### This project demonstrates the creation of a backend api using Python Flask and json dataset. 
- **app.py** is the Flask app
- **app_tests.py** contains the unittests using Pytest
- **playlist.json** is the json dataset
- **requirements.txt** are the packages required to run everything.

# Instructions for Execution

- [Python 3.12.2](https://www.python.org/downloads/release/python-3122/) is this project's version.
- **Run** `pip install -r requirements.txt` for the packages.
  - **Recommended:** Create and activate a [python virtual environment](https://docs.python.org/3/library/venv.html) first.
- **Run** `flask run` to start the local server.
  - *NOTE:* `flask run` *defaults to 'app' so if for some reason it doesn't work, use* `flask --app app run` *instead, I never ran into issues however.* 
  - Use CTRL + C to quit the server at any time.
- By default, the Flask server runs at http://127.0.0.1:5000. You can navigate to the respective routes from there.
  - *For example: http://127.0.0.1:5000/api/data*
- From the server, the following **routes** are possible:
  - `/api/data`
    - Pagination is implemented. 
    - `/api/data?page={int}` 
      - `{int}` is an integer valid from 1 through 10.
  - `/api/data/<title>` 
    - `<title>` is the title of a song.
  - `/api/data/<title>/<column>`
    - `<title>` is the title of a song.
    - `<column>` is an attribute of the song.
  - `/api/data/rating/<int: rating>`
    - `<int: rating>` is an integer valid from 1 through 5.
    - *NOTE: If no rating is given, this returns the column value.*
- To execute the unit tests, run `pytest app_tests.py`.