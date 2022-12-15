import os

def command(mof_dir):
    return F'docker run --rm -it -v $PWD/{mof_dir}:/app raspa simulate simulation.input'

directories = [d for d in os.listdir() if os.path.isdir(d)]

with open('tasks.sh', 'w') as f:
    f.writelines([command(d) + '\n' for d in directories])