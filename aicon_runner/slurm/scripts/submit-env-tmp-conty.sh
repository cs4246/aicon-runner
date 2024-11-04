#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={stdout_file}
#SBATCH --error={stderr_file}
#SBATCH --partition={partition}
#SBATCH --gpus={gpus}
#SBATCH --time={slurm_time_limit}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem={slurm_memory_limit}
#SBATCH --qos=normal
#SBATCH --mail-type=ALL

set -e

CONTY="{conty}"

TMP_DIR="/tmp/aicon"
ENV_PATH="$TMP_DIR/{env_name}"

PACKAGES="{packages}"
SUBMISSION="{submission}"

OUTPUT_PATH="{output_json_path}"
OUTPUT_DIR="$(dirname $OUTPUT_PATH)"
OUTPUT_FILENAME="$(basename $OUTPUT_PATH)"

RUNTIME_LIMIT={run_time_limit}s

CONTAINER_ENV_PATH="/tmp/env"
CONTAINER_SUBMISSION_PATH="/tmp/submission.zip"

mkdir -p $TMP_DIR

/usr/bin/python -m venv --copies "$ENV_PATH"

source "$ENV_PATH/bin/activate"

python -m pip install --upgrade pip setuptools
python -m pip install --no-cache-dir $PACKAGES

export SANDBOX=1
export SANDBOX_LEVEL=2
export DISABLE_NET=1
export HOME_DIR="$OUTPUT_DIR"

$CONTY --bind $ENV_PATH $CONTAINER_ENV_PATH --ro-bind $SUBMISSION $CONTAINER_SUBMISSION_PATH $CONTAINER_ENV_PATH/bin/python -m pip install --no-index --no-build-isolation $CONTAINER_SUBMISSION_PATH

vm_current=$(free -m -t | grep Total | awk -F ' ' '{print $3}')
vm_total=$((vm_current + {run_memory_limit}))
ulimit -v $vm_total

timeout -k $RUNTIME_LIMIT -s 9 -v $RUNTIME_LIMIT $CONTY --bind $ENV_PATH $CONTAINER_ENV_PATH $CONTAINER_ENV_PATH/bin/python -m aicon_evaluator -o $OUTPUT_FILENAME
