# aiVLE Runner

A program designed to monitor and execute submissions and test suites from aiVLE.

This version is a rewrite of the original aiVLE Runner, now utilizing Celery for better jobs management and performance.

## Dependencies

* Python >= 3.12
* Celery

## Usage

1. Duplicate the `example.env` file to create a new `.env` file.
2. Update the values in the `.env` file according to your aivle-web configuration.
3. Ensure that the user `AIVLE_USERNAME` is registered as an admin in the system.
4. Install the requirements:
```
pip install -r requirements.txt
```
5. Run watcher
```
python -m aivle_runner
```

You can also specify the number of concurrent processes using the following command:
```
python -m aivle_runner --concurrency 5
```
