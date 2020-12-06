# Mutation Utilites
# 12/4/2020
# reevesbra@outlook.com

import random
import string

class Mutator:

    def random_char(self):
        ''' Parameters
            ----------
            self: Mutator object
            
            Returns
            _______
            random character
        '''
        vocab = string.punctuation + string.ascii_letters + string.digits
        return random.choice(vocab)

    def randomize_char(self, string):
        ''' Parameters
            ----------
            self: Mutator object
            string: string to mutate
            
            Returns
            _______
            output: mutated string
        '''
        length = len(string)
        position = random.randint(0, length - 1)
        char_after = self.random_char()
        output = string[:position] + char_after + string[position + 1:]
        return output

    def delete_char(self, string):
        ''' Parameters
            ----------
            self: Mutator object
            string: string to mutate
            
            Returns
            _______
            output: mutated string
        '''
        length = len(string)
        position = random.randint(0, length - 1)
        output = string[:position] + string[position + 1:]
        return output

    def insert_char(self, string):
        ''' Parameters
            ----------
            self: Mutator object
            string: string to mutate
            
            Returns
            _______
            output: mutated string
        '''
        output = string
        length = len(string)
        position = random.randint(0, length - 1)
        random_char = self.random_char()
        output = string[:position] + random_char + string[position:]
        return output

    def swap_chars(self, string):
        ''' Parameters
            ----------
            self: Mutator object
            string: string to mutate
            
            Returns
            _______
            output: mutated string
        '''
        length = len(string)
        position1 = random.randint(0, length - 1)
        position2 = random.randint(0, length - 1)
        char1 = string[position1]
        char2 = string[position2]

        if position1 == position2:
            return string
        
        min_position = min(position1, position2)
        max_position = max(position1, position2)
        output = string[:min_position] + string[max_position] + string[min_position + 1:max_position] + string[min_position] + string[max_position + 1:]
        return output

    def mutate(self, string, num_mutations=3):
        ''' Parameters
            ----------
            self: Mutator object
            string: string to mutate
            num_mutations: number of mutations to make
            
            Returns
            _______
            output: mutated string
        '''
        output = string
        mutations = [self.randomize_char, self.delete_char, self.insert_char, self.swap_chars]
        for i in range(num_mutations):
            current_mutation = random.choice(mutations)
            output = current_mutation(output)
        return output
