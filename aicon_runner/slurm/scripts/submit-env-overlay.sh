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

source "{base_env_dir}/bin/activate"

OVERLAY_PYTHON_VERSION=$({overlay_env_dir}/bin/python --version | cut -d' ' -f2- | cut -d'.' -f1,2)
export PYTHONPATH="{overlay_env_dir}/lib/python$OVERLAY_PYTHON_VERSION/site-packages":$PYTHONPATH

runner -o "{output_json_path}"
