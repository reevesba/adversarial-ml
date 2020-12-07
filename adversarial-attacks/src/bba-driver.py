# Black Box Attack Driver
# 12/6/2020
# reevesbra@outlook.com

import blackboxattack as bba

def main():
    api_key = ""
    model_id  = "d16f390eb32cad478c7ae150069bd2c6"
    target_goal = 0
    num_iters = 1000
    learning_rate = 0.005
    h = 0.005

    image_path = "input/coffee.jpg"
    output_dir = "output/"

    attack = bba.BlackBoxAttack(api_key, model_id, target_goal, num_iters, learning_rate, h)
    attack.execute_attack(image_path, output_dir)

if __name__ == "__main__":
    main()
