docker run --rm -it -v $PWD/MOF-A:/app raspa simulate simulation.input
docker run --rm -it -v $PWD/MOF-B:/app raspa simulate simulation.input
docker run --rm -v $PWD:/app raspa rm -rf */Movies/ */VTK/ */Restart