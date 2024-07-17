#!/bin/bash
#SBATCH --job-name=download

#SBATCH --array=0-39
#SBATCH --tasks=1
#SBATCH --cpus-per-task=4
#SBATCH --output=/proj/cvl/users/x_juska/slurm_logs/slurm-%A_%a_%x.out
#SBATCH --error=/proj/cvl/users/x_juska/slurm_logs/slurm-%A_%a_%x.err
# TOTAL MEMORY PER NODE
#SBATCH --mem=4G 

echo "SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"


task_per_job=250 # this number is the total number of tiles divided by the number of jobs (~ 1,300,000 / 4)
start_from=$((SLURM_ARRAY_TASK_ID * task_per_job))
end_at=$((start_from + task_per_job))


python main_download.py start_from=$start_from end_at=$end_at



