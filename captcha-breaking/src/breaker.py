# Captcha Breaking Bot
# 12/3/2020
# reevesbra@outlook.com

import utilities
import time
import urllib.request
import pickle
import numpy as np
from selenium import webdriver
from keras.models import Sequential
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.core import Flatten, Dense

class BreakerBot:

    def __init__(self):
        ''' Parameters
            ----------
            self: BreakerBot object
            
            Returns
            _______
            None
        '''
        self.util = utilities.Utilities()

    def __captcha_to_char_pipeline(self, file_path):
        ''' Parameters
            ----------
            self: BreakerBot object
            file_path: location of char image
            
            Returns
            _______
            char_images: array of char images
        '''
        captcha_image = self.util.read_image(file_path)

        # transform image
        transformed_image = self.util.to_grayscale(captcha_image)
        transformed_image = self.util.threshold_image(transformed_image)
        transformed_image = self.util.dilate_chars(transformed_image)

        # get contours for extracting characters
        image_contours = self.util.find_contours(transformed_image)

        # create and save character images
        char_bounding_rects = self.util.split_rects(self.util.compute_bounding_rects(image_contours))
        char_bounding_rects = self.util.sort_bounding_rects(char_bounding_rects)
        char_images = self.util.get_char_images(char_bounding_rects, captcha_image)

        return char_images

    def __load_classifier(self):
        ''' Parameters
            ----------
            self: BreakerBot object
            
            Returns
            _______
            model: CNN
        '''
        num_classes = 32

        model = Sequential()
        model.add(Conv2D(20, (5, 5), padding="same", input_shape=(20, 20, 1), activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Conv2D(50, (5, 5), padding="same", activation="relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        model.add(Dense(512, activation="relu"))
        model.add(Dense(num_classes, activation="softmax"))

        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

        model.load_weights("out/weights.h5")
        return model
        

    def __load_label_binarizer(self):
        ''' Parameters
            ----------
            self: BreakerBot object
            
            Returns
            _______
            label binarizer object
        '''
        return pickle.load(open("out/binarizer.pkl", "rb"))

    def __load_model(self):
        ''' Parameters
            ----------
            self: BreakerBot object
            
            Returns
            _______
            model: CNN classifier
            label_binarizer: label binarizer object
        '''
        model = self.__load_classifier()
        label_binarizer = self.__load_label_binarizer()
        return model, label_binarizer

    def __predict_chars(self, char_images, model, label_binarizer):
        ''' Parameters
            ----------
            self: BreakerBot object
            char_images: array of char images
            model: CNN classfier
            label_binarizer: label binarizer object
            
            Returns
            _______
            predicted_text: class predictions
        '''
        X = []
        for char_image in char_images:
            image = self.util.to_grayscale(char_image)
            image = self.util.normalize(image)
            image = self.util.reshape(image)
            X.append(image)

        X = np.array(X, dtype="float")/255.0
        pred = model.predict(X)
        predicted_text = label_binarizer.inverse_transform(pred)
        return predicted_text

    def execute(self):
        ''' Parameters
            ----------
            self: BreakerBot object
            
            Returns
            _______
            None
        '''
        model, label_binarizer = self.__load_model()

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)
        driver.get("https://ml4cs.com/CAPTCHA/index/php/break-me-use-a-bot-to-crack-the-captcha/")
        time.sleep(2)

        captcha_image = driver.find_element_by_css_selector(".wpcf7-captcha-captcha-170")
        src = captcha_image.get_attribute("src")
        urllib.request.urlretrieve(src, "captcha.png")

        char_images = self.__captcha_to_char_pipeline("captcha.png")
        pred = self.__predict_chars(char_images, model, label_binarizer)

        captcha_input = driver.find_element_by_name("captcha-170")
        captcha_input.send_keys(pred)
        captcha_input.submit()
        time.sleep(5)
        driver.quit()

        
