import os
from dotenv import load_dotenv

load_dotenv()

broker_transport = os.getenv("CELERY_BROKER_TRANSPORT")
broker_user = os.getenv("CELERY_BROKER_USER")
broker_password = os.getenv("CELERY_BROKER_PASSWORD")
broker_host = os.getenv("CELERY_BROKER_HOST")
broker_port = os.getenv("CELERY_BROKER_PORT")

aivle_url = os.getenv("AIVLE_URL")
aivle_username = os.getenv("AIVLE_USERNAME")
aivle_password = os.getenv("AIVLE_PASSWORD")
aivle_force_https = bool(int(os.getenv("AIVLE_FORCE_HTTPS", 0)))
aivle_verify = bool(int(os.getenv("AIVLE_VERIFY", 0)))

runner_runner_kit_path=os.getenv("RUNNER_RUNNER_KIT_PATH", "git+https://github.com/cs4246/aivle-runner-kit.git")
runner_runs_path=os.getenv("RUNNER_RUNS_PATH", "./runs")
runner_testsuites_path=os.getenv("RUNNER_TESTSUITES_PATH", "./testsuites")
runner_submissions_path=os.getenv("RUNNER_SUBMISSIONS_PATH", "./submissions")

slurm_enable=bool(int(os.getenv("SLURM_ENABLE")))
slurm_venv_directory=os.getenv("SLURM_VENV_DIRECTORY", "./venvs")
slurm_venv_time_limit=int(os.getenv("SLURM_VENV_TIME_LIMIT"))
slurm_venv_force=bool(int(os.getenv("SLURM_VENV_FORCE")))
slurm_run_partition=os.getenv("SLURM_RUN_PARTITION", "normal")
slurm_run_time_limit=int(os.getenv("SLURM_RUN_TIME_LIMIT"))
slurm_run_memory_limit=int(os.getenv("SLURM_RUN_MEMORY_LIMIT"))

os.makedirs(runner_runs_path, exist_ok=True)
os.makedirs(runner_testsuites_path, exist_ok=True)
os.makedirs(runner_submissions_path, exist_ok=True)
os.makedirs(slurm_venv_directory, exist_ok=True)
