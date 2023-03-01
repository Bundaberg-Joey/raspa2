import os
from glob import glob

from tqdm import tqdm

from utils import xe_kr_input, calc_min_image_indices


# -------------------------------------------------------------------------------------
cutoff_radii = [12, 14, 16, 18]
repeats = 3
docker_line = 'tsp hare run --rm -d -v $PWD:/app crh53/raspa2 '
out_dir = 'results'

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

print('Copying over raspa template files...')
os.system(F'cp raspa_template/* {out_dir}')  # copy FF files
print('completed !')
print('Copying cif files across...')
os.system(F'cp cifs/*.cif {out_dir}')  # copy all cif files
print('completed!')

cifs = glob(F'{out_dir}/*.cif')


tasks = []
print('Writing task files...')
for cif_file in tqdm(cifs):
    mof_name = os.path.basename(cif_file)

    for radii in cutoff_radii:
        na, nb, nc = calc_min_image_indices(cif_file, radii)
        
        for i in range(repeats):
            
            k = F'{mof_name}_{radii}_{i}'
            sim_file_name = F'simulation_{k}.input'
            content = xe_kr_input(mof_name, na, nb, nc)
            
            with open(os.path.join(out_dir, sim_file_name), 'w') as f:
                f.writelines(content)
            
            tasks.append(F'{docker_line} simulate {sim_file_name} -a {k} \n')
            
print('completed!')

with open(os.path.join(out_dir, 'tasks.sh'), 'w') as f:
    f.write(tasks)
            
# ------------------------------------------------------------------------------------
