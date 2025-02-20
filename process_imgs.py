from natsort import natsorted, ns
import os
import shutil
from skimage.transform import resize, rescale
from skimage.io import imsave, imread
import numpy as np
import cv2

SCALE = 0.6

source = 'raw_images'
dest = 'processed_images'

classes = ['capacitor', 'potentiometer', 'led', 'diode', 'resistor', 'integrated_circuit', 'transistor', 'switch', 'inductor', 'jumper']
items = 5
angulos = ['V1', 'V2']
cores = ['B', 'W']

if not os.path.exists(source):
    print(f"Não existe caminho para pasta de entrada ({source})")
    exit(0)

if not os.path.exists(dest):
    print(f"Não existe caminho para pasta de resultado ({dest})")
    print(f"Criando diretório {dest}")
    os.mkdir(dest)

x = os.listdir(source)
files = natsorted(x, alg=ns.IGNORECASE)
# print(files)

def rename_images():
    atual = 0
    for i, classe in enumerate(classes):
        if os.path.exists(os.path.join(dest, classe)):
            print(f'{os.path.join(dest, classe)} já existe, pulando')
            continue
        os.mkdir(os.path.join(dest, classe))
        for item in range(1, items+1):
            for l, cor in enumerate(cores):
                for k, angulo in enumerate(angulos):
                    # os.rename(os.path.join(source, files[atual]), os.path.join(os.path.join(dest, classe), f'{i:02d}' + '-' f'{item:02d}' + '-' + angulo + '-' + cor + '.png'))
                    try:
                        shutil.copy(os.path.join(source, files[atual]), os.path.join(os.path.join(dest, classe), f'{i:02d}' + '-' f'{item:02d}' + '-' + angulo + '-' + cor + '.jpg'))
                        atual += 1
                    except IndexError: 
                        print(f'Acabaram as imagens. ({atual} imagens processadas)')
                        return
    print(f'Todas {atual} imagens processadas')

def process_images():
    for i, classe in enumerate(classes):
        atual = 0
        classe_folder = os.path.join(dest, classe)
        
        if not os.path.exists(classe_folder):
            print(f'{classe_folder} não existe')
            break
        print(f'Processando {classe} ({i+1}/{len(classes)})')
        files = os.listdir(classe_folder)
        for name in files:
            imagem = imread(os.path.join(classe_folder, name))

            imagem = imagem[812:(4624-812), 436:(3472-436)]

            # im = resize(imagem, [4624*SCALE, 3472*SCALE])
            im = rescale(imagem, 0.5, channel_axis=2, anti_aliasing=True)
            im = ((im * 255).astype(np.uint8))
            # print(im.shape)

            # imsave(os.path.join(classe_folder, name[:-3]+'png'), im)
            
            # Mais rapido do que imsave
            im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
            cv2.imwrite(os.path.join(classe_folder, name[:-3]+'png'), im)
            
            os.remove(os.path.join(classe_folder, name))
            atual += 1
    print("Completado")

def main():
    rename_images()
    process_images()

if __name__ == "__main__":
    main()
