# Captcha PreProcessing
# 12/3/2020
# reevesbra@outlook.com

import os
import cv2
import utilities

class PreProcessor:

    def __init__(self, directory):
        ''' Parameters
            ----------
            self: PreProcessor object
            directory: location of captcha images
            
            Returns
            _______
            None
        '''
        if directory != "":
            self.captchas = self.__extract_captchas(directory)
        else:
            self.captchas = None
            print("No directory, program may not work as intended.")

        self.util = utilities.Utilities()

    def __extract_captchas(self, directory):
        ''' Parameters
            ----------
            self: PreProcessor object
            directory: name of folder containing captchas
            
            Returns
            _______
            array of files in directory
        '''
        return [os.path.join(directory, f) for f in os.listdir(directory)]

    def __get_label(self, image):
        ''' Parameters
            ----------
            self: PreProcessor object
            image: captcha image
            
            Returns
            _______
            label: captcha in plain text
        '''
        filename = os.path.basename(image)
        label = filename.split(".")[0]
        return label

    def __to_array(self, image):
        ''' Parameters
            ----------
            self: PreProcessor object
            image: captcha image
            
            Returns
            _______
            captcha image as array
        '''
        return cv2.imread(image)

    def preprocess(self):
        ''' Parameters
            ----------
            self: PreProcessor object
            
            Returns
            _______
            None
        '''
        output_dir = "dat/char_images"
        char_counts = {}

        for image in self.captchas:
            captcha_label = self.__get_label(image)
            captcha_image = self.__to_array(image)

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

            for char_image, current_char in zip(char_images, captcha_label):
                if len(char_images) == 4:
                    save_dir = os.path.join(output_dir, current_char)
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir)
                    char_count = char_counts.get(current_char, 0)
                    image_save_path = os.path.join(save_dir, str(char_count) + ".png")
                    cv2.imwrite(image_save_path, char_image)
                    char_counts[current_char] = char_count + 1


