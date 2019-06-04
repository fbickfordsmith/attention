import os
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

'''
Use a pretrained VGG16 to classify ImageNet examples.

Reference: https://medium.com/@vijayabhaskar96/tutorial-image-classification-
    with-keras-flow-from-directory-and-generators-95f75ebe5720
'''

import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator

# use decode_predictions to get predicted classes
# we know true classes from folders

model = VGG16(weights='imagenet')
path = '/mnt/fast-data16/datasets/ILSVRC/2012/clsloc/val_white/'
datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
generator = datagen.flow_from_directory(
    directory=path,
    target_size=(224, 224),
    batch_size=1,
    shuffle=False, # False => returns images in order
    class_mode=None) # None => returns just images (no labels)

true_classes = generator.classes
img_paths = generator.filenames
name2ind = generator.class_indices
ind2name = {ind:name for name, ind in name2ind.items()}
true_names = np.array([ind2name[ind] for ind in true_classes])

predicted_classes = []
for i, img_path in enumerate(img_paths):
    if i % 2000 == 0:
        print(f'{i:05} images processed')
    img = load_img(path+img_path, target_size=(224, 224))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    predicted_classes.append(np.argmax(model.predict(img)))

predicted_names = np.array([ind2name[ind] for ind in predicted_classes])
correct = (predicted_names==true_names)
accuracy = np.mean(correct)
print(f'Top-1 accuracy: {(accuracy*100):.2f}%')
