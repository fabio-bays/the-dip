from natsort import natsorted, ns
import os
import shutil
from skimage.transform import resize, rescale
from skimage.io import imsave, imread
import numpy as np


source = 'raw_images'
dest = 'processed_images'

classes = ['capacitor', 'potentiometer', 'led', 'diode', 'resistor', 'integrated_circuit', 'transistor', 'switches', 'inductors', 'jumpers']
items = 5
angulos = ['V1', 'V2']
cores = ['B', 'W']

if not os.path.exists(source):
    print(f"não existe caminho para pasta de entrada ({source})")
    exit(0)

if not os.path.exists('dest'):
    print(f"não existe caminho para pasta de resultado ({dest})")
    os.mkdir(dest)

x = os.listdir(source)
files = natsorted(x, alg=ns.IGNORECASE)
# print(files)

def rename_images():
    atual = 0
    for i, classe in enumerate(classes):
        os.mkdir(os.path.join(dest, classe))
        for item in range(1, items+1):
            for k, angulo in enumerate(angulos):
                for l, cor in enumerate(cores):
                    # os.rename(os.path.join(source, files[atual]), os.path.join(os.path.join(dest, classe), f'{i:02d}' + '-' f'{item:02d}' + '-' + angulo + '-' + cor + '.png'))
                    try:
                        shutil.copy(os.path.join(source, files[atual]), os.path.join(os.path.join(dest, classe), f'{i:02d}' + '-' f'{item:02d}' + '-' + angulo + '-' + cor + '.jpg'))
                        atual += 1
                    except IndexError: 
                        print(f'Acabaram as imagens ({atual+1} imagens processadas)')
                        return

rename_images()

for i, classe in enumerate(classes):
    atual = 0
    classe_folder = os.path.join(dest, classe)
    if not os.path.exists(classe_folder):
        print(f'{classe_folder} não existe')
        break
    files = os.listdir(classe_folder)
    for name in files:
        imagem = imread(os.path.join(classe_folder, name))
        
        # imagem = imagem[0:1000, 0:1000]
        # print(f'original: \n{imagem}')
        # im = rescale(imagem, 0.8)
        im = resize(imagem, (2312, 1736))
        # print(f'scaled: \n{im}')
        im = ((im * 255).astype(np.uint8))
        # print(f'scaled mul: \n{im}')

        imsave(os.path.join(classe_folder, name[:-3]+'png'), im)
        os.remove(os.path.join(classe_folder, name))
        atual += 1


