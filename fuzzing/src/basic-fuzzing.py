# Basic Fuzzing
# 12/4/2020
# reevesbra@outlook.com
# introduces code fuzzing/coverage

import string as s
import random
import sys
import inspect

def toy_fuzzer(max_len=150, punctuation=True, letters=True, digits=True):
    vocabulary = (punctuation*s.punctuation + letters*s.ascii_letters + digits*s.digits)
    output_len = random.randrange(0, max_len + 1)
    out = [random.choice(vocabulary) for i in range(0, output_len)]
    return "".join(out)

def cgi_decode(input):
    output = ""
    i = 0

    while i < len(input):
        current_char = input[i]
        if current_char == "+":
            # replace '+' with ' '
            output += " "
        elif current_char == "%":
            # replace '%xx' with char of hex number xx
            digit_high, digit_low = input[i + 1], input[i + 2]
            i += 2
            try:
                v = int(digit_high, 16)*16 + int(digit_low, 16)
                output += chr(v)
            except:
                raise ValueError("Invalid Input")
        else:
            output += current_char
        i += 1
    return output

def line_tracer(frame, event, arg):
    if event == "line":
        lineno = frame.f_lineno
        global coverage
        coverage.add(lineno)
    return line_tracer

def record_coverage(function, s):
    global coverage
    coverage = set([])
    sys.settrace(line_tracer)
    function(s)
    sys.settrace(None)
    coverage = frozenset(coverage)
    return coverage

def code_coverage(string):
    record_coverage(cgi_decode, string)
    cgi_decode_code = inspect.getsource(cgi_decode)
    cgi_decode_lines = [""] + cgi_decode_code.splitlines()
    
    function_start = 16

    for i in range(len(cgi_decode_lines)):
        line = cgi_decode_lines[i]
        if i + function_start in coverage:
            print(line)
        else:
            print("#" + line)

def main():
    # toy fuzzer test
    for i in range(0, 5):
        print("Run " + str(i + 1) + ": " + toy_fuzzer() + "\n")

    # code coverage test
    test_strings = ["cgi+enconding", "%63%67%69%2Dencoding", "cgi4encoding"]
    for i in range(len(test_strings)):
        print("Run " + str(i + 1) + ":")
        code_coverage(test_strings[i])
        print()

if __name__ == '__main__':
	main()
