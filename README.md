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

## Fugacitiy info
* [Patrick Barrie's program for solving cubic equations of state](https://pjb10.user.srcf.net/thermo/pure.html) was used to arrive at the below fugacities
* Data regarding critical points and accentric factors for the calculation were taken from the `Xe` and `Kr` files provided by the hMOF database (themselves taken from NIST)

|Material|Temperature|Pressure|Fugacity|
|:--:|:--:|:--:|:--:|
|Xe|273|1.0|0.9924|
|Kr|273|1.0|0.9967|
|Xe|273|5.0|0.9623|
|Kr|273|5.0|0.9837|
|Xe|273|10.0|0.9253|
|Kr|273|10.0|0.9671|