#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={stdout_file}
#SBATCH --error={stderr_file}
#SBATCH --partition={partition}
#SBATCH --time={time_limit}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem={memory_limit}
#SBATCH --qos=normal
#SBATCH --mail-type=ALL

set -e

ENV_PATH="/tmp/{env_name}"

/usr/bin/python -m venv --copies "$ENV_PATH"

source "$ENV_PATH/bin/activate"

python -m pip install --upgrade pip
python -m pip install --no-cache-dir {packages}

runner -o "{output_json_path}"
