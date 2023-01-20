# Simmer The Toads

This is the primary Python module that will comprise our application.

The existing files/directories serve the following functions:

- `views.py`: This is where all the major routes of our app will live. This can
  be split into smaller submodules if need be.
- `static/`: Contains public CSS, JS, images, and other publicly viewable
  assets.
- `templates/`: Contains Jinja2 templates for HTML generation.
- `tests/`: Contains unit and integration testing assets.

## Developer Environment Setup

1.  Install [Python 3.8](https://www.python.org/downloads/) or later.

2.  Navigate to the root of this repository then create and activate a virtual
    environment.

        $ python3 -m venv env
        $ source env/bin/activate # mac/linux
        $ env/bin/activate.bat    # windows

3.  Install the project dependencies.

        $ pip install .

4.  Start the development web server.

        $ flask --debug --app SimmerTheToads run

5.  Navigate to `http://localhost:5000` to access the webapp.

## Useful Links

- ![Flask Applications as Packages](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)
- ![Flask Organization Patterns](https://exploreflask.com/en/latest/organizing.html)
- ![Flask General Documentation](https://flask.palletsprojects.com/en/2.2.x/)
