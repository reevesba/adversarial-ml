# Black Box Attack on Clarif.ai
# 12/6/2020
# reevesbra@outlook.com

from clarifai.rest import ClarifaiApp
import cv2
import numpy as np
import random

class BlackBoxAttack:

    def __init__(self, api_key, model_id, goal_coordinate, num_iters, learning_rate, h):
        ''' Parameters
            __________
            api_key: clarifai api key
            model_id: clarifai public model
            goal_coordinate: classification goal
            num_iters: number of times to perturb image
            learning_rate: step size
            h: approximation of derivative

            Returns
            _______
            None
        '''
        self.API_KEY = api_key
        self.MODLE_ID  = model_id
        self.GOAL_COORDINATE = goal_coordinate
        self.NUM_ITERS = num_iters
        self.LEARNING_RATE = learning_rate
        self.H = h
        self.coordinates = []
        self.coordinate_numbering = {}
        self.coordinate_numbering_rev = {}

    def set_coordinates(self, image):
        ''' Parameters
            __________
            image: image used to get coordinates

            Returns
            _______
            None
        '''
        index = 0
        for i in range(image.shape[1]):
            for j in range(image.shape[0]):
                self.coordinate_numbering[tuple((i, j))] = index
                self.coordinate_numbering_rev[index] = tuple((i, j))
                index += 1
        self.coordinates = list(self.coordinate_numbering.values())

    def is_better(self, goal_coordinate, delta):
        ''' Parameters
            __________
            goal_coordinate: coordinate we want to work towards
            delta: change in prediction score

            Returns
            _______
            True if change is less than 0
            False otherwise
        '''
        return delta[goal_coordinate] < 0

    def save_image(self, image, path):
        ''' Parameters
            __________
            image: image to save
            path: where to save image

            Returns
            _______
            None
        '''
        cv2.imwrite(path, image)

    def minus_h_image(self, image, coordinate):
        ''' Parameters
            __________
            image: image to perturb
            coordinate: random coordinate in image

            Returns
            _______
            minus_image: image with one pixel lightened
        '''
        minus_image = image.copy()
        minus_image[self.coordinate_numbering_rev[coordinate]] = (minus_image[self.coordinate_numbering_rev[coordinate]] - self.H)
        return minus_image

    def plus_h_image(self, image, coordinate):
        ''' Parameters
            __________
            image: image to perturb
            coordinate: random coordinate in image

            Returns
            _______
            plus_image: image with one pixel darkened
        '''
        plus_image = image.copy()
        plus_image[self.coordinate_numbering_rev[coordinate]] = (plus_image[self.coordinate_numbering_rev[coordinate]] + self.H)
        return plus_image

    def pick_random_coordinate(self):
        ''' Parameters
            __________
            None

            Returns
            _______
            Random coordinate
        '''
        return np.random.choice(self.coordinates, 1)[0]

    def image_to_predictions(self, image_path, model):
        ''' Parameters
            __________
            image_path: path to image used for prediction
            model: clarifai model

            Returns
            _______
            final_dict: score for each category
        '''
        response = model.predict_by_filename(image_path)
        concepts = response["outputs"][0]["data"]["concepts"]

        scores_dict = {}
        for concept in concepts:
            scores_dict[concept["name"]] = concept["value"]
        final_dict = [scores_dict["safe"], scores_dict["suggestive"], scores_dict["explicit"], scores_dict["drug"], scores_dict["gore"]]
        return np.asarray(final_dict)

    def execute_attack(self, image_path, output_dir):
        ''' Parameters
            __________
            image_path: location of image to perturb
            output_dir: where to store perturbed images

            Returns
            _______
            None
        '''
        app = ClarifaiApp(api_key=self.API_KEY)
        model = app.models.get(model_id=self.MODLE_ID )

        image = cv2.imread(image_path)
        image = cv2.resize(image, (50, 50))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = image.astype(np.float32)/255

        self.set_coordinates(image)

        for i in range(self.NUM_ITERS):
            image_save_path = output_dir + "current_image" + str(i) + ".jpg"
            self.save_image(image*255, image_save_path)
            current_score = self.image_to_predictions(image_save_path, model)

            print("Iteration " + str(i) + " score:")
            print(current_score)

            chosen_coordinate = self.pick_random_coordinate()
            plus_or_minus = bool(random.getrandbits(1))

            if plus_or_minus:
                plus_image = self.plus_h_image(image, chosen_coordinate)
                self.save_image(plus_image*255, output_dir + "plus_image.jpg")
                plus_prediction = self.image_to_predictions(output_dir + "plus_image.jpg", model)
                delta = plus_prediction - current_score

                print("Iteration " + str(i) + " delta:")
                print(delta)

                if self.is_better(self.GOAL_COORDINATE, delta):
                    image[self.coordinate_numbering_rev[chosen_coordinate]] += self.LEARNING_RATE
            else:
                minus_image = self.minus_h_image(image, chosen_coordinate)
                self.save_image(minus_image*255, output_dir + "minus_image.jpg")
                minus_prediction = self.image_to_predictions(output_dir + "minus_image.jpg", model)
                delta = minus_prediction - current_score

                print("Iteration " + str(i) + " delta:")
                print(delta)

                if self.is_better(self.GOAL_COORDINATE, delta):
                    image[self.coordinate_numbering_rev[chosen_coordinate]] -= self.LEARNING_RATE



