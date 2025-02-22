import os
import shutil
from ultralytics.data.utils import autosplit

autosplit(path='augmented_dataset', weights=(0.8, 0.1, 0.1))

classes = ['capacitor', 'potentiometer', 'led', 'diode', 'resistor', 'integrated_circuit', 'transistor', 'switch', 'inductor', 'jumper']

foldrs = ['test', 'train', 'val']

for fil in foldrs:
    for classe in classes:
        os.makedirs(os.path.join(fil, classe), exist_ok=True)

    with open('autosplit_' + fil + '.txt') as f:
        for line in f:
            line = line[:-1]
            dest = line.replace('images', 'datasets/dip/'+fil)
            shutil.copy(line, dest)
            try:
                shutil.copy(line[:-3]+'txt', dest[:-3]+'txt')
            except:
                try:
                    shutil.copy(line[:-8]+'.txt', dest[:-3]+'txt')
                except:
                    shutil.copy(line[:-9]+'.txt', dest[:-3]+'txt')