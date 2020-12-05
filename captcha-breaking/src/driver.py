# Captcha Breaking Driver
# 12/3/2020
# reevesbra@outlook.com

import preprocessor as p
import model
import breaker

def main():
    # generate char data
    processor = p.PreProcessor("dat/captcha_images")
    processor.preprocess()

    # build/train the model
    adv_model = model.CNN("dat/char_images")
    adv_model.create_model()

    # break site captcha
    bot = breaker.BreakerBot()
    bot.execute()

if __name__ == '__main__':
	main()
