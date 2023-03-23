# Simmer The Toads

This is the primary Python module that will comprise our application. This
module is responsible for all the authenticated Spotify API calls, playlist
analysis/reordering, and serving the React frontend.

The existing notable files/directories serve the following functions:

- `views.py`: This is where all the major routes of our app will live. This can
  be split into smaller submodules if need be.
- `engine.py`: Contains Flask agnostic Spotify integration (playlist
  interactions, analysis, reordering, etc.).
- `tests/`: Contains unit and integration testing assets.

## Backend Developer Environment Setup

1.  Install [Python 3.8](https://www.python.org/downloads/) or later.

2.  Navigate to the root of this repository then create and activate a virtual
    environment.

    ```cli
    $ python3 -m venv env
    $ source env/bin/activate # mac/linux
    $ env/bin/activate.bat    # windows
    ```

3.  Install the project dependencies.

    ```cli
    $ pip install .
    ```

4.  Start the development web server.

    ```cli
    $ flask --debug --app SimmerTheToads run
    ```

5.  Navigate to `http://127.0.0.1:5000/api` to access the WebAPI.

    > Do not use 'localhost' in place of 127.0.0.1. Authentication relies on the
    > origin to remain consistent between the backend and frontend.

## Production Deployment

1. Build the React frontend. From the root of the repository:

   ```cli
   $ cd frontend
   $ npm ci
   $ npm build
   ```

2. Try running the Flask application independent of NodeJS. From the root of the
   repository:

   ```cli
   $ flask --debug --app SimmerTheToads run
   ```

   Navigating to `http://127.0.0.1:5000` should render the entire frontend
   correctly, without having to start the NodeJS development environment.

3. Update the relevant information within `.env` Most notably, the redirect URI
   is almost certainly different between debug and production builds.

4. Try starting the application with gunicorn directly.

   ```cli
   $ pip install gunicorn
   $ gunicorn SimmerTheToads:app
   ```

   Navigating to `http://127.0.0.1:5000` should render the entire frontend
   correctly.

## Useful Links

- [Flask Applications as Packages](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
- [Flask Organization Patterns](https://exploreflask.com/en/latest/organizing.html)
- [Flask General Documentation](https://flask.palletsprojects.com/en/2.2.x/)
