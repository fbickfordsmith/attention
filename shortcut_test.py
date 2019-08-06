import os
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '3'

from models import build_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from models_vgg2 import build_vgg2
import time

data_partition = 'train'
path_data = f'/mnt/fast-data16/datasets/ILSVRC/2012/clsloc/{data_partition}/'
path_activations = '/home/freddie/activations-conv/'

def steps(num_examples, batch_size):
    return int(np.ceil(num_examples/batch_size))

datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

params_generator = dict(
    class_mode='sparse',
    target_size=(224, 224),
    batch_size=256,
    shuffle=True)

params_testing = dict(
    use_multiprocessing=True,
    verbose=True)

generator0 = datagen.flow_from_directory(
    directory=path_data,
    **params_generator)

generator1 = datagen.flow_from_directory(
    directory=path_activations,
    **params_generator)

time0 = time.time()
model0 = build_model()
buildtime0 = time.time()-time0

time0 = time.time()
model1 = build_vgg2()
buildtime1 = time.time()-time0

time0 = time.time()
scores0 = model0.evaluate_generator(
    generator=generator0,
    steps=steps(generator0.n, generator0.batch_size),
    **params_testing)
epochtime0 = time.time()-time0

time0 = time.time()
scores1 = model1.evaluate_generator(
    generator=generator1,
    steps=steps(generator1.n, generator1.batch_size),
    **params_testing)
epochtime1 = time.time()-time0

print(f'''
OLD MODEL
build time = {int(buildtime0)} seconds
epoch time = {int(epochtime0)} seconds
scores = {scores0}
{model0.metrics_names}

NEW MODEL
build time = {int(buildtime1)} seconds
epoch time = {int(epochtime1)} seconds
scores = {scores1}
{model1.metrics_names}
''')