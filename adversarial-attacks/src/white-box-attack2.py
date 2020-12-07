# Another White Box Attack
# 12/6/2020
# reevesbra@outlook.com

import mnistmodel
import keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from foolbox.models import KerasModel
from foolbox.v1 import attacks
keras.backend.set_learning_phase(0)

def main():
    # model wont work with eager execution enable
    tf.compat.v1.disable_eager_execution()

    batch_size = 128
    num_classes = 10
    epochs = 12

    model = mnistmodel.MnistModel(batch_size, num_classes, epochs)
    white_box = model.build_model()

    x_sample, y_sample = model.get_samples()

    #image_plot = plt.imshow(np.reshape(x_sample*255, (28, 28)))
    #plt.show()

    # no attack
    label = np.argmax(white_box.predict(np.reshape(x_sample, (1, 28, 28, 1))), axis=-1)[0]
    label = np.asarray(label)
    print(label)

    # attack
    preprocessing = dict(flip_axis=-1)
    fmodel = KerasModel(white_box, bounds=(0, 255), preprocessing=preprocessing)

    attack = attacks.FGSM(fmodel)
    adversarial = attack(x_sample, y_sample)

    image_plot = plt.imshow(np.reshape(adversarial, (28, 28)))
    plt.show()

    label = np.argmax(white_box.predict(np.reshape(adversarial, (1, 28, 28, 1))), axis=-1)[0]
    print(label)

if __name__ == "__main__":
    main()
