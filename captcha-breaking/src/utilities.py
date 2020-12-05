# Captcha Breaking Utilities
# 12/3/2020
# reevesbra@outlook.com

import cv2
import numpy as np
import imutils

WHITE = (255, 255, 255)

class Utilities:

    @staticmethod
    def display_image(image):
        ''' Parameters
            ----------
            image: captcha image
            
            Returns
            _______
            None
        '''
        cv2.imshow("window name", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def to_grayscale(image):
        ''' Parameters
            ----------
            image: captcha image as array
            
            Returns
            _______
            None
        '''
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def threshold_image(image):
        ''' Parameters
            ----------
            image: grayscaled captcha image
            
            Returns
            _______
            thresholded captcha image
        '''
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    @staticmethod
    def dilate_chars(image):
        ''' Parameters
            ----------
            image: thresholded captcha image
            
            Returns
            _______
            dilated captcha image
        '''
        kernel = np.ones((2, 2), np.uint8) 
        return cv2.dilate(image, kernel, iterations = 1)

    @staticmethod
    def find_contours(image):
        ''' Parameters
            ----------
            image: dilated captcha image
            
            Returns
            _______
            captcha image contours
        '''
        return cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    @staticmethod
    def compute_bounding_rects(contours):
        ''' Parameters
            ----------
            contours: captcha image contours
            
            Returns
            _______
            bounding rectangles
        '''
        return list(map(cv2.boundingRect, contours))

    @staticmethod
    def show_bounding_rects(rects, image):
        ''' Parameters
            ----------
            rects: bounding rectangles
            image: captcha image
            
            Returns
            _______
            None
        '''
        for rect in rects:
            x, y, w, h = rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        __display(image)

    @staticmethod
    def split_rects(rects):
        ''' Parameters
            ----------
            rects: bounding rectangles
            
            Returns
            _______
            char_bounding_rects: bounding rectangles of chars
        '''
        char_bounding_rects = []
        for rect in rects:
            (x, y, w, h) = rect
            if w/h > 1.25:
                half_width = int(w/2)
                char_bounding_rects.append((x, y, half_width, h))
                char_bounding_rects.append((x + half_width, y, half_width, h))
            else:
                char_bounding_rects.append(rect)
        return char_bounding_rects

    @staticmethod
    def get_char_images(rects, image):
        ''' Parameters
            ----------
            rects: char bounding rectangles
            image: captcha image
            
            Returns
            _______
            char_images: images of characters
        '''
        char_images = []
        for rect in rects:
            x, y, w, h = rect
            char_image = image[y - 1:y + h + 1, x - 1:x + w + 1]
            char_images.append(char_image)
        return char_images

    @staticmethod
    def sort_bounding_rects(rects):
        ''' Parameters
            ----------
            rects: bounding rectangles
            
            Returns
            _______
            sorted bounding rectangle list
        '''
        return(sorted(rects, key = lambda x: float(x[0])))

    @staticmethod
    def read_image(file_path):
        ''' Parameters
            ----------
            file_path: location of char image
            
            Returns
            _______
            character image
        '''
        return cv2.imread(file_path)

    @staticmethod
    def normalize(image, desired_width=20, desired_height=20):
        ''' Parameters
            ----------
            image: captcha image
            desired_width: scaled width
            desired_height: scaled height
            
            Returns
            _______
            scaled image
        '''
        (h, w) = image.shape[:2]

        if w > h:
            image = imutils.resize(image, width=desired_width)
        else:
            image = imutils.resize(image, height=desired_height)

        width_padding = int((desired_width - image.shape[1])/2)
        height_padding = int((desired_height - image.shape[0])/2)

        new_image = cv2.copyMakeBorder(image, height_padding, height_padding, width_padding, width_padding, cv2.BORDER_CONSTANT, value=WHITE)
        new_image = cv2.resize(new_image, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

        return new_image

    @staticmethod
    def reshape(image):
        ''' Parameters
            ----------
            image: char image
            
            Returns
            _______
            char image reshaped for keras
        '''
        return np.expand_dims(image, axis=2)


