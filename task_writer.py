import os

def command(mof_dir):
    return F'docker run --rm -it -v $PWD/{mof_dir}:/app raspa simulate simulation.input'

directories = [d for d in os.listdir() if os.path.isdir(d)]
commands = [command(d) + '\n' for d in directories]
commands += ['docker run --rm -v $PWD:/app raspa rm -rf */Movies/ */VTK/ */Restart']  # not needed

with open('tasks.sh', 'w') as f:
    f.writelines(commands)