import json
import os
import traceback

from celery import shared_task
from .web import AiconAPI
from .utils import safe_filename
from . import config, slurm

STATUS_ERROR = 'E'
STATUS_DONE = 'D'

aicon = AiconAPI(config.aicon_url, auth_token=config.aicon_auth_token,
                 force_https=config.aicon_force_https, verify=config.aicon_verify)

@shared_task
def evaluate(task_data: dict, submission_data: dict):
    response = aicon.job_run(submission_data)
    response.raise_for_status()

    # Define filepaths
    task_path = os.path.join(config.runner_tasks_path, f"{safe_filename(task_data['name'])}-{task_data['id']}.zip")
    submission_path = os.path.join(config.runner_submissions_path, f"{submission_data['id']}.zip")
    evaluator_path = config.runner_evaluator_path

    try:
        # Download packages
        response = aicon.download_package(task_data, task_path)
        response.raise_for_status()
        response = aicon.download_package(submission_data, submission_path)
        response.raise_for_status()

        # Run
        result = slurm.run(
            task_path,
            submission_path,
            evaluator_path,
            time_limit = task_data["run_time_limit"] or config.slurm_run_time_limit,
            memory_limit = task_data["memory_limit"] or config.slurm_run_memory_limit,
            task_id = task_data["id"],
            submission_id = submission_data["id"],
            partition = task_data["partition_name"] or config.slurm_run_partition,
            gpus = task_data["gpus"],
            base_dir = config.runner_runs_path,
            venv_base_dir = config.slurm_venv_directory,
            force = config.slurm_venv_force,
            use_slurm = config.slurm_enable,
            slurm_time_limit = config.slurm_run_time_limit,
            slurm_memory_limit = config.slurm_run_memory_limit,
        )
        notes = result
        submission_data['point'] = result['point']
        submission_data['status'] = STATUS_DONE
    except Exception as e:
        notes = {
            "error": {
                "type": str(type(e).__name__),
                "args": [str(earg) for earg in list(e.args)],
                # "trace": traceback.format_exc()
            }
        }
        submission_data['point'] = None
        submission_data['status'] = STATUS_ERROR

    submission_data['notes'] = json.dumps(notes)

    response = aicon.job_end(submission_data)
    assert response.ok, response
