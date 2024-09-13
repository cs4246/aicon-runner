# aicon Runner

A program designed to monitor and execute submissions and test suites from aicon.

This version is a rewrite of the original aicon Runner, now utilizing Celery for better jobs management and performance.

## Dependencies

* Python >= 3.12
* Celery

## Usage

1. Duplicate the `example.env` file to create a new `.env` file.
2. Update the values in the `.env` file according to your aicon-web configuration.
3. Ensure that the `AICON_AUTH_TOKEN` is associated with an admin user in the system.
4. Install the requirements:
```
pip install -r requirements.txt
```
5. Run watcher
```
python -m aicon_runner
```

You can also specify the number of concurrent processes using the following command:
```
python -m aicon_runner --concurrency 5
```
