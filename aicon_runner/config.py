import os
from dotenv import load_dotenv

load_dotenv()

broker_transport = os.getenv("CELERY_BROKER_TRANSPORT")
broker_user = os.getenv("CELERY_BROKER_USER")
broker_password = os.getenv("CELERY_BROKER_PASSWORD")
broker_host = os.getenv("CELERY_BROKER_HOST")
broker_port = os.getenv("CELERY_BROKER_PORT")

aicon_url = os.getenv("AICON_URL")
aicon_auth_token = os.getenv("AICON_AUTH_TOKEN")
aicon_force_https = bool(int(os.getenv("AICON_FORCE_HTTPS", 0)))
aicon_verify = bool(int(os.getenv("AICON_VERIFY", 0)))

runner_evaluator_path=os.getenv("RUNNER_EVALUATOR_PATH", "git+https://github.com/cs4246/aicon-evaluator.git")
runner_runs_path=os.getenv("RUNNER_RUNS_PATH", "./runs")
runner_tasks_path=os.getenv("RUNNER_TASKS_PATH", "./tasks")
runner_submissions_path=os.getenv("RUNNER_SUBMISSIONS_PATH", "./submissions")

slurm_enable=bool(int(os.getenv("SLURM_ENABLE")))
slurm_venv_directory=os.getenv("SLURM_VENV_DIRECTORY", None)
slurm_venv_time_limit=int(os.getenv("SLURM_VENV_TIME_LIMIT"))
slurm_venv_force=bool(int(os.getenv("SLURM_VENV_FORCE")))
slurm_run_partition=os.getenv("SLURM_RUN_PARTITION", "normal")
slurm_run_time_limit=int(os.getenv("SLURM_RUN_TIME_LIMIT"))
slurm_run_memory_limit=int(os.getenv("SLURM_RUN_MEMORY_LIMIT"))

if slurm_venv_directory == "":
    slurm_venv_directory = None

os.makedirs(runner_runs_path, exist_ok=True)
os.makedirs(runner_tasks_path, exist_ok=True)
os.makedirs(runner_submissions_path, exist_ok=True)
if slurm_venv_directory is not None:
    os.makedirs(slurm_venv_directory, exist_ok=True)
