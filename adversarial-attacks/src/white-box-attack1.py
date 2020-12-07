# White Box Attack using foolbox
# 12/6/2020
# reevesbra@outlook.com

import keras
from keras.applications.resnet50 import ResNet50
import foolbox # using version 2.4.0
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

def main():
    # model wont work with eager execution enable
    tf.compat.v1.disable_eager_execution()

    resnet_model = ResNet50(weights="imagenet")
    preprocessing = dict(flip_axis=-1, mean=np.array([104, 116, 123]))
    fmodel = foolbox.models.KerasModel(resnet_model, bounds=(0, 255), preprocessing=preprocessing)

    image, label = foolbox.utils.imagenet_example()
    imgplot = plt.imshow(image/255)
    plt.title("Image 1")
    plt.show()
    print("Classification 1: ", np.argmax(fmodel.forward_one(image)))

    # use fast gradient signed method
    attack = foolbox.v1.attacks.FGSM(fmodel)
    adversarial = attack(image, label)
    imgplot = plt.imshow(adversarial / 255)
    plt.title("Image 2")
    plt.show()
    print("Classification 2: ", np.argmax(fmodel.forward_one(adversarial)))

if __name__ == "__main__":
    main()



