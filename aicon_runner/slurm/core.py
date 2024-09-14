import hashlib
import os
import subprocess
import shutil
import json
import time
import logging
from ..utils import hash_str, hash_file_path
from .exceptions import MalformedOutputError, RunnerError, SuiteInstallError, AgentInstallError
from typing import Optional


BASE_PATH = os.path.dirname(os.path.realpath(__file__))
SCRIPTS_DIR = os.path.join(BASE_PATH, 'scripts')
SCRIPT_CREATE_ENV = os.path.join(SCRIPTS_DIR, 'create-venv.sh')
SCRIPT_SUBMIT_ENV_OVERLAY = os.path.join(SCRIPTS_DIR, 'submit-env-overlay.sh')
SCRIPT_SUBMIT_ENV_TMP = os.path.join(SCRIPTS_DIR, 'submit-env-tmp.sh')


def to_slurm_time(seconds: Optional[int] = None) -> str:
    if seconds is None:
        return ''
    assert seconds <= 24*3600, f"Time conversion only works up to 24 hours: {seconds}"
    slurm_time = time.strftime('%H:%M:%S', time.gmtime(seconds))
    return slurm_time


def to_slurm_memory(memory: Optional[int] = None) -> str:
    if memory is None:
        return "0"
    return f"{memory}K"


def create_venv(
        env_name: str,
        packages: list[str] = [],
        python_dir: Optional[str] = '/usr/',
        base_dir: str = '.',
        time_limit: Optional[int] = None,
        force: bool = False,
        use_slurm: bool = True,
    ) -> str:
    env_dir = os.path.join(base_dir, env_name)
    print(f'==> {env_dir}')
    if os.path.exists(env_dir) and not force:
        print('Using existing virtual environment.')
        return env_dir

    subprocess.call(["chmod", "u+x", SCRIPT_CREATE_ENV], stderr=subprocess.DEVNULL)
    cmd = [SCRIPT_CREATE_ENV, python_dir, env_dir] + packages
    if use_slurm:
        cmd = ["srun", f"--time={to_slurm_time(time_limit)}"] + cmd

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line, end="")
    for stderr_line in iter(popen.stderr.readline, ""):
        print(stderr_line, end="")
    popen.stdout.close()
    return_code = popen.wait()

    if return_code:
        shutil.rmtree(env_dir)
        raise subprocess.CalledProcessError(return_code, cmd)
    return env_dir


def run(
        testsuite_path: str,
        submission_path: str,
        runner_kit_path: str,
        time_limit: Optional[int] = 600,
        memory_limit: Optional[int] = 0,
        testsuite_id: Optional[int] = None,
        submission_id: Optional[int] = None,
        partition: str = "",
        base_dir: str = "./runs",
        venv_base_dir: Optional[str] = "./venvs",
        force: bool = False,
        use_slurm: bool = True,
        slurm_time_limit: Optional[int] = 3600,
    ) -> dict:
    run_id = f"{testsuite_id}-{submission_id}" if testsuite_id is not None and submission_id is not None else str(time.time())
    output_dir = os.path.join(base_dir, run_id)
    os.makedirs(output_dir, exist_ok=True)
    stdout_file = os.path.join(output_dir, 'stdout.log')
    stderr_file = os.path.join(output_dir, 'stderr.log')
    output_json_path = os.path.join(output_dir, 'output.json')
    submit_script_path = os.path.join(output_dir, 'submit.sh')

    config = {
        'job_name': run_id,
        'stdout_file': stdout_file,
        'stderr_file': stderr_file,
        'output_json_path': output_json_path,
        'partition': partition,
        'slurm_memory_limit': to_slurm_memory(memory_limit),
    }

    if venv_base_dir is None:
        config['env_name'] = hash_str(run_id)
        config['packages'] = ' '.join([runner_kit_path, testsuite_path, submission_path])
        config['slurm_time_limit'] = to_slurm_time(slurm_time_limit)
        config['run_time_limit'] = str(time_limit)
    else:
        config['slurm_time_limit'] = to_slurm_time(slurm_time_limit)
        config['run_time_limit'] = str(time_limit)
        base_env_name = hash_file_path(testsuite_path)
        try:
            config['base_env_dir'] = create_venv(base_env_name, packages=[runner_kit_path, testsuite_path], base_dir=venv_base_dir, force=force, use_slurm=use_slurm)
        except Exception as e:
            raise SuiteInstallError(e)

        env_name = hash_file_path(submission_path)
        try:
            config['overlay_env_dir'] = create_venv(env_name, packages=[submission_path], base_dir=venv_base_dir, force=force, use_slurm=use_slurm)
        except Exception as e:
            raise AgentInstallError(e)

    print(config)

    template_submit_script_path = SCRIPT_SUBMIT_ENV_TMP if venv_base_dir is None else SCRIPT_SUBMIT_ENV_OVERLAY
    with open(template_submit_script_path, 'r') as f:
        script = f.read()
    for k, v in config.items():
        script = script.replace(f"{{{k}}}", str(v))
    with open(submit_script_path, 'w') as f:
        f.write(script)

    subprocess.call(["chmod", "u+x", submit_script_path])
    cmd = [submit_script_path]
    if use_slurm:
        cmd = ["sbatch", "-W"] + cmd
        return_code = subprocess.call(cmd)
    else:
        with open(stdout_file, 'w') as f_stdout, open(stderr_file, 'w') as f_stderr:
            return_code = subprocess.call(cmd, stdout=f_stdout, stderr=f_stderr)

    stdout, stderr = '', ''
    if os.path.isfile(stdout_file):
        with open(stdout_file, 'r') as f:
            stdout = f.read()
    if os.path.isfile(stderr_file):
        with open(stderr_file, 'r') as f:
            stderr = f.read()

    print(stdout if return_code == 0 else stderr)

    if return_code:
        raise RunnerError(stdout, stderr)

    try:
        with open(output_json_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise MalformedOutputError(str(e), stdout)

    return data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('testsuite_path')
    parser.add_argument('submission_path')
    parser.add_argument('runner_kit_path')
    parser.add_argument('-p', '--partition', default="")
    parser.add_argument('-t', '--time-limit', default=600)
    parser.add_argument('-m', '--memory-limit', default=0)
    parser.add_argument('-a', '--submission-id', default=None)
    parser.add_argument('-s', '--testsuite-id', default=None)
    parser.add_argument('-e', '--venv-base-dir', default=None)
    parser.add_argument('--force', action=argparse.BooleanOptionalAction)
    parser.add_argument('--use-slurm', action=argparse.BooleanOptionalAction)
    args = parser.parse_args()

    output = run(
        args.testsuite_path,
        args.submission_path,
        args.runner_kit_path,
        partition=args.partition,
        venv_base_dir=args.venv_base_dir,
        time_limit=args.time_limit,
        memory_limit=args.memory_limit,
        submission_id=args.submission_id,
        testsuite_id=args.testsuite_id,
        force=args.force,
        use_slurm=args.use_slurm,
    )

    print(output)
