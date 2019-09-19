# -*- coding: utf-8 -*-
"""Kvasir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UEjLjkdLCwMSKXhG-QinLPhLfsfPqrYY
"""

class file_write:
    import os

    def __init__(self,file_name,Address=os.getcwd()):
        self.Address=Address+file_name
        print(self.Address)
        #Address = "C:/Users/kirut/Documents/Project Prime/"
        self.file = open(self.Address,'w')

    def write(self,n,new_line=True):
        if new_line == True:
            write_string = str(n)+'\n'
        else:
            write_string = str(n)
        self.file.write(write_string)

    def close(self):
        self.file.close()


class file_read:
    import os

    def __init__(self,file_name,Address=os.getcwd()):
        self.Address=Address+file_name
        print(self.Address)
        self.file = open(self.Address,'r')

    def read(self,new_line=True,dtype=int):
        self.lines = []
        for line in self.file:
            if new_line == True:
                line = line.strip()
            self.lines.append(dtype(line))
        return self.lines

    def close(self):
        self.file.close()

class divider:
    def __init__(self,data,test_percentage=10):
        self.data = data
        self.test_percentage=test_percentage

    def test(self):
        return(self.data[:int(len(self.data)*self.test_percentage/100)])

    def train(self):
        return(self.data[int(len(self.data)*self.test_percentage/100):])

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/gdrive')
# %cd /gdrive

import glob
import os

class content_reader:
    def __init__(self,address):
        self.address = address+'/'

    def read_file_names(self):
        if True:
            out = []
            for r, d, f in os.walk(self.address):
                for folder in f:
                    out.append(os.path.join(r, folder))
            #for filename in glob.glob(self.address):
            #    print(filename)
            #    out.append(filename)
            return out
        else:
            print("Address has got no files or it is not a folder")
            return out

    def read_folder_names(self):
        if True:
            out = []
            for r, d, f in os.walk(self.address):
                for folder in d:
                    out.append(os.path.join(r, folder))
            #for filename in glob.glob(self.address):
            #    print(filename)
            #    out.append(filename)
            return out
        else:
            print("Address has got no files or it is not a folder")
            return out

    def read_text(self,output_type="LIST",strip=True):

        try:
            file = open(self.address,'r')
            if output_type.upper() == "LIST":
                out = []
                for line in file:
                    if strip == True:
                        out.append(line.strip)
                    else:
                        out.append(line)
            elif output_type.upper() == "TEXT":
                out = file.read()
            return out
        except:
            print("NOT A TEXT FILE")

    def read_image(self,output_type="NP_ARRAY",size="Default"):
        self.address = self.address[:-1]
        import PIL
        image = PIL.Image.open(self.address)
        if size != "Default":
            self.size = size
            image = image.resize(size,PIL.Image.ANTIALIAS)
        else:
            self.size=image.size
        if output_type=="NP_ARRAY":
            import numpy as np
            array = np.asarray(image)
            return array
        else:
            return image

import numpy as np
import random
class organize:
    def __init__(self,location):
        self.input_location = location

    def read_files(self):
        input_location = self.input_location
        input_files = content_reader(input_location)
        input_files_names = input_files.read_folder_names()
        X_datas = []
        Y_datas = []
        ref = {}
        i=0
        n = 0
        print(len(input_files_names))
        for file in input_files_names:
            ref[file]=i
            i+=1
        for file in input_files_names:
            file_location = file
            file_obj = content_reader(file_location)
            print(file_location)
            images = file_obj.read_file_names()
            for image_name in images:
                n+=1
                image_location = image_name
                image = content_reader(image_location)
                image_data = image.read_image(size=(331,331))
                X_datas.append(image_data)
                Y_datas.append(ref[file])
                print(float(n)/4000*100)
        total_number_of_data = len(Y_datas)
        zero = list(range(0,total_number_of_data-1))
        random.shuffle(zero)
        shuffled = zero
        #print(shuffled)
        X=[]
        Y=[]
        for i in shuffled:
            X.append(X_datas[i])
            Y.append(Y_datas[i])
        return([X,Y])

base_dir = os.path.join('','/gdrive/My Drive/Kvasir/kvasir-dataset')
train_dir = os.path.join(base_dir,'Train')
validation_dir = os.path.join(base_dir,'Validation')

train_dyed_lifted_polyps = os.path.join(train_dir,'dyed-lifted-polyps')
train_dyed_resection_margins = os.path.join(train_dir,'dyed_resection_margins')
train_esophagitis = os.path.join(train_dir,'esophagitis')
train_normal_cecum = os.path.join(train_dir,'normal-cecum')
train_normal_pylorus = os.path.join(train_dir,'normal-pylorus')
train_normal_z_line = os.path.join(train_dir,'normal-z-line')
train_polyps = os.path.join(train_dir,'polyps')
train_ulcerative_colitis = os.path.join(train_dir,'ulcerative-colitis')

validation_dyed_lifted_polyps = os.path.join(validation_dir,'dyed-lifted-polyps')
validation_dyed_resection_margins = os.path.join(validation_dir,'dyed_resection_margins')
validation_esophagitis = os.path.join(validation_dir,'esophagitis')
validation_normal_cecum = os.path.join(validation_dir,'normal-cecum')
validation_normal_pylorus = os.path.join(validation_dir,'normal-pylorus')
validation_normal_z_line = os.path.join(validation_dir,'normal-z-line')
validation_polyps = os.path.join(validation_dir,'polyps')
validation_ulcerative_colitis = os.path.join(validation_dir,'ulcerative-colitis')

print('total training polyps images:', len(os.listdir(train_polyps)))

from tensorflow import keras
import tensorflow as tf

image_size = 331 # All images will be resized to 160x160
batch_size = int(len(os.listdir(validation_polyps)))
batch_size = 32
print(batch_size)

# Rescale all images by 1./255 and apply image augmentation
train_datagen = keras.preprocessing.image.ImageDataGenerator(
                rescale=1./255)

validation_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
                train_dir,  # Source directory for the training images
                target_size=(image_size, image_size),
                batch_size=batch_size,
                # Since we use binary_crossentropy loss, we need binary labels
                class_mode='categorical')

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = validation_datagen.flow_from_directory(
                validation_dir, # Source directory for the validation images
                target_size=(image_size, image_size),
                batch_size=batch_size,
                class_mode='categorical')

IMG_SHAPE = (image_size, image_size,3)

base_model = tf.keras.applications.MobileNet(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

base_model.trainable = False

base_model.summary()

model = tf.keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(8,activation='sigmoid')
])

initial_learning_rate = 0.1
decay_step = 10000
decay_rate = 1/10
global_step = tf.Variable(0,trainable=False,name="global_step")
learning_rate = tf.train.exponential_decay(initial_learning_rate,global_step,decay_step,decay_rate)
optimizer = tf.train.AdamOptimizer(0.1)

model.compile(optimizer=optimizer,
             loss='categorical_crossentropy',
             metrics=['categorical_accuracy'])

model.summary()

len(model.trainable_variables)

epochs = 10
steps_per_epoch = train_generator.n
validation_steps = validation_generator.n

history = model.fit_generator(train_generator,
                             steps_per_epoch = steps_per_epoch,
                             epochs = epochs,
                             workers = 4,
                             validation_data = validation_generator,
                             validation_steps = validation_steps)

import matplotlib.pyplot as plt
import matpllotlb.image as mpimg

acc = history.history['acc']
val_acc = history.history['val_acc']

loss = history.history['loss']
val_loss = history.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.ylabel('Accuracy')
plt.ylim([min(plt.ylim()),1])
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.ylabel('Cross Entropy')
plt.ylim([0,max(plt.ylim())])
plt.title('Training and Validation Loss')
plt.show()

base_model.trainable = True

print(len(base_model.layers))
fine_tune_at = int(len(base_model.layers)*90/100)
for layer in base_model.layers[:fine_tune_at]:
  layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=0.0001),
             loss='mean_squared_error',
             metrics=['accuracy'])

model.summary()

len(model.trainable_variable)

history_fine = model.fit_generator(train_generator,
                             steps_per_epoch = steps_per_epoch,
                             epochs = epochs,
                             workers = 4,
                             validation_data = validation_generator,
                             validation_steps = validation_steps)

acc += history_fine.history['acc']
val_acc += history_fine.history['val_acc']

loss += history_fine.history['loss']
val_loss += history_fine.history['val_loss']

plt.figure(figsize=(8, 8))
plt.subplot(2, 1, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.ylim([0.9, 1])
plt.plot([epochs-1,epochs-1], plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(2, 1, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.ylim([0, 0.2])
plt.plot([epochs-1,epochs-1], plt.ylim(), label='Start Fine Tuning')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

