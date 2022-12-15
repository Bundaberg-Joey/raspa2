# Raspa2 - Docker set  up for running raspa simulations
## Usage
1. Build the docker image `docker build -t raspa .`
2. Create a directory containing any file relevant for a `raspa` simulation i.e. all `.def` files, `.cif` file of framework, and the `simulation.input` file
3. Each individual simulation to be run must be wthin it's own directory, i.e. so if `MOF-A` and `MOF-B` are different mofs for the same simulation there will be two different directories
4. Once created, run the `task_writer.py` file in the directory continig the subdirectories
5. This will produce a task file which can then be used to run the simulations sequentially 

## Demonstration
The below commands should create an `Output` directory in each of the subdirectories containing the simulation output.

```bash
docker build -t raspa .
cd demo
sh demo_tasks.sh
```
