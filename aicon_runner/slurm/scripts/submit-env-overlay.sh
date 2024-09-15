#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={stdout_file}
#SBATCH --error={stderr_file}
#SBATCH --partition={partition}
#SBATCH --time={slurm_time_limit}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem={slurm_memory_limit}
#SBATCH --qos=normal
#SBATCH --mail-type=ALL

set -e

source "{base_env_dir}/bin/activate"

OVERLAY_PYTHON_VERSION=$({overlay_env_dir}/bin/python --version | cut -d' ' -f2- | cut -d'.' -f1,2)
export PYTHONPATH="{overlay_env_dir}/lib/python$OVERLAY_PYTHON_VERSION/site-packages":$PYTHONPATH

vm_current=$(free -m -t | grep Total | awk -F ' ' '{print $3}')
vm_total=$((vm_current + {run_memory_limit}))
ulimit -v $vm_total

timeout -k {run_time_limit}s -s 9 -v {run_time_limit}s runner -o "{output_json_path}"
