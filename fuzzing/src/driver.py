# EvoFuzzer Driver
# 12/5/2020
# reevesbra@outlook.com

import evofuzz

def main():
    carrying_capacity = 100
    seed = ["http://www.google.com/search?q=fuzzing", "http://www.google.com/search;q=fuzzinb2g", "http://www.Xgole.com/eaHrh;qfu/zzingb2g"]
    mutation_prob = 0.1

    fuzzer = evofuzz.EvolutionaryFuzzer(carrying_capacity, seed, mutation_prob)

    number_of_generations = 50
    samples = fuzzer.fuzz(number_of_generations)

    important_samples = samples[0]
    coverage_dict = samples[1]

    for i in range(len(important_samples)):
        print(important_samples[i])
    
    for key, value in coverage_dict.items():
        print(str(key) + " => " + str(value))

if __name__ == '__main__':
	main()
