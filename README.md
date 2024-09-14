# aicon Runner

A program designed to monitor and execute submissions and test suites from aicon.

This version is a rewrite of the original aicon Runner, now utilizing Celery for better jobs management and performance.

## Dependencies

* Python >= 3.12
* Celery

## Usage

1. Duplicate the `example.env` file to create a new `.env` file.
2. Update the values in the `.env` file according to your aicon-web configuration.
3. Install the requirements:
```
pip install -r requirements.txt
```
4. Run watcher
```
python -m aicon_runner
```

You can also specify the number of concurrent processes using the following command:
```
python -m aicon_runner --concurrency 5
```

## Notes

* Ensure that the `AICON_AUTH_TOKEN` is associated with an admin user in the system.
* If `SLURM_VENV_DIRECTORY` is set, you must first run a single job (submission) to initialize the task environment. Submitting multiple jobs simultaneously may lead to race conditions during environment setup.
* `RUNNER_RUNNER_KIT_PATH` must be either a zip file or a valid Git URL pointing to a GitHub repository.
