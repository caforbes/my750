# My 750 Journal

This app is designed for a single user to write a daily journal, with encouragement to reach a word count target. The built in target is 750 words per day.

## Run your own

1. Ensure you have a working version of Python 3.12 installed.

    ```sh
    python --version
    # Python 3.12.4
    ```

    Pyenv is recommended to manage multiple Python versions. [Find setup instructions here.](https://github.com/pyenv/pyenv)

2. This app uses `pipenv` for environment and dependency management. First, upgrade your local `pip` installation.

    ```sh
    pip install --upgrade pip
    ```

    Install or upgrade `pipenv` following [the package instructions here](https://pipenv.pypa.io/en/latest/installation.html).
    Then, from the root `my750` directory, use `pipenv` to install local dependencies.

    ```sh
    pipenv install
    ```

3. Ensure you have Postgres installed for your local database. Find [downloads here](https://www.postgresql.org/download/) and [installation instructions here](https://www.postgresql.org/docs/current/tutorial-install.html).

4. Install [dbmate](https://github.com/amacneil/dbmate) for handy database management.
5. Set required environment variables:
    * `DATABASE_URL`: This is a url that lists the desired database and connection configuration to use. [Instructions are in the dbmate docs here.](https://github.com/amacneil/dbmate?tab=readme-ov-file#postgresql)

6. To run the application:
    1. Ensure the Postgres server is running (e.g. by running `sudo service postgresql start`).
    2. Open the virtual environment with `pipenv shell` (or your preferred method).
    3. Ensure the database is up to date with `dbmate up`
    4. Run the app with `flask run`
    5. View the running application at [localhost:5000](http://localhost:5000)

## Testing and development

### Setup

1. Follow all the previously listed setup instructions.
2. Use `pipenv` to install local dependencies, including **dev packages**.

    ```sh
    pipenv install --dev
    # Installing dependencies from Pipfile.lock
    # To activate this project's virtualenv, run pipenv shell.
    # Alternatively, run a command inside the virtualenv with pipenv run.
    ```

<!-- TODO: set up precommit or GHA for requirements checks and/or test running
3. Inside the virtual environment, install pre-commit hooks.

    ```sh
    pipenv run pre-commit install
    ``` -->

4. Set up additional environment variables for testing.
    * `TEST_DATABASE_URL`: Like DATABASE_URL, but points to a separate database for integration testing. [Instructions are in the dbmate docs here.](https://github.com/amacneil/dbmate?tab=readme-ov-file#postgresql)

### Run tests

Tests are in the `/tests` directory and use Pytest. Make commands have been defined to include setup for the test database.

Run tests:

```sh
make test
```

<!-- TODO: Run tests and show a coverage report in the terminal:

```sh
make coverage
``` -->

### Run the app

Serve the app locally for development at [localhost:5000](http://localhost:5000):

```sh
flask run --debug
# ...
# * Running on http://127.0.0.1:5000/
# Press CTRL+C to quit
```
