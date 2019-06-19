'''
Take a CSV where each row is a set of ImageNet class names
(eg, ['n01440764', ...]). For each set, i,
- Move the folders for the in-set classes into a new folder called `seti`.
- In the `seti` folder, create empty folders for all out-of-set classes.

Arguments:
- folder in {'train', 'val', 'val_white'}

References:
- thispointer.com/how-to-create-a-directory-in-python/
- thispointer.com/python-how-to-move-files-and-directories/
'''

import os
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import sys, shutil, numpy

folder = sys.argv[1] # sys.argv[0] is the name of the script
class_sets = numpy.loadtxt('csv/class_sets.csv', dtype=str, delimiter=',')
path_to_data = '/home/freddie/ILSVRC2012/clsloc/'+folder+'/'
# path_to_data = 'ILSVRC2012/ILSVRC2012_img_val_copy/'
print(f'Running {sys.argv[0]} on {path_to_data}')

for i, inset_classes in enumerate(class_sets):
    set_folder = f'set{i:02}/'
    for inset_class in inset_classes:
        # move inset_class folder to the folder for this set
        shutil.move(
            path_to_data+inset_class, # source path
            path_to_data+set_folder+inset_class) # destination path

    # np.setdiff1d(a, b) returns unique values in a that are not in b
    outofset_classes = np.setdiff1d(class_sets, inset_classes)
    for outofset_class in outofset_classes:
        # make new empty folders for all classes not in this set
        os.makedirs(path_to_data+set_folder+outofset_class)

# Copying a folder using bash:
# old_folder contains a, b, c
# With no slash:
#     cp -r .../old_folder .../new_folder => new_folder contains old_folder
# With slash:
#     cp -r .../old_folder/ .../new_folder => new_folder contains a, b, c
# cp -r /mnt/fast-data16/datasets/ILSVRC/2012/clsloc/ /home/freddie/ILSVRC2012
