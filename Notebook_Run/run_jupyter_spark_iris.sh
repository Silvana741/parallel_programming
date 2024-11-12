#!/bin/bash -l


#SBATCH --job-name="Jupyter_job_aion"

#SBATCH --output=Notebooks_logs/AION/notebook_%j.log

#SBATCH -p batch
#SBATCH -N 1
#SBATCH --ntasks-per-node 64  # Optimized for 1 full node of aion
#SBATCH -c 1

#SBATCH --time=8:00:00


    
## other options
## Move to the directory where the job was submitted
#cd $SLURM_SUBMIT_DIR


print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
module purge || print_error_and_exit "No 'module' command"
# Python 3.X by default (also on system)


module use /work/projects/software_stack_alpha/easybuild/aion/2023b/epyc/modules/all
module load devel/Spark/3.5.1-foss-2023b-Java-17
export JAVA_HOME=$JAVA_HOME
export PATH=$JAVA_HOME/bin:$PATH
export SPARK_HOME=/work/projects/software_stack_alpha/easybuild/aion/2023b/epyc/software/Spark/3.5.1-foss-2023b-Java-17
export PATH=$SPARK_HOME/bin:$PATH
module purge 
source ~/environments/distributed_forecasting/bin/activate

python --version
# export PYSPARK_PYTHON=~/environments/distributed_forecasting/bin/python
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"

#module avail
#jupyter notebook --ip $(facter ipaddress) --no-browser  &
jupyter lab --ip $(ip addr | egrep '172\.17|21'| grep 'inet ' | awk '{print $2}' | cut -d/ -f1) --no-browser &
pid=$!
sleep 5s
jupyter notebook list
jupyter --paths
jupyter kernelspec list
#echo "Enter this command on your laptop: ssh -p 8022 -NL 8888:$(facter ipaddress):8888 clee@access-iris.uni.lu" > notebook.log
echo "Enter this command on your laptop: ssh -p 8022 -NL 8888:$(ip addr | egrep '172\.17|21'| grep 'inet ' | awk '{print $2}' | cut -d/ -f1)" > notebook.log
wait $pid