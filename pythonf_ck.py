import argparse
from collections import Counter
from itertools import product

import os

import sys
from pyminifier import minification, token_utils

LINE_SEP = ';'  # \n optional


def floor_to_tens(x):
    return int(x / 10) * 10


def init_numbers(hist):
    """
    Initiates dictionary containing values for used variables
    :param hist: histogram of most used characters in source code
    :return: string containing initiation for used variables and dictionary with possible values
    """
    chars = 'exc'
    variables = dict()

    count = 1
    hist_count = 0
    result = "c='%c'" + LINE_SEP  # init formatting string
    result += 'e=+(()==())' + LINE_SEP  # move one to e
    for l in range(2, 4):
        for perm in product(chars, repeat=l):
            perm = ''.join(perm)
            if count < 10:
                variables[count] = perm
                if count == 1:
                    result += perm + '=e' + LINE_SEP
                else:
                    result += variables[count] + '=' + variables[count - 1] + '+e' + LINE_SEP
                count += 1
            elif count < 130:
                variables[count] = perm
                if count == 10:
                    result += variables[count] + '=' + variables[count - 1] + '+e' + LINE_SEP
                    result += 'e=' + variables[10] + LINE_SEP  # move ten to e
                else:
                    result += variables[count] + '=' + variables[count - 10] + '+e' + LINE_SEP
                count += 10
            else:
                # characters with number below 10 or multiplicity of 10 shouldn't be saved in temporary variables
                while hist_count < len(hist) \
                        and (ord(hist[hist_count][0]) <= 10
                             or ord(hist[hist_count][0]) % 10 == 0):
                    hist_count += 1
                if hist_count >= len(hist):
                    break
                char = hist[hist_count][0]
                num = ord(char)
                variables[char] = perm
                result += perm + '=c%(' + variables[num % 10] + '+' + variables[floor_to_tens(num)] + ')' + LINE_SEP
                hist_count += 1

    return result, variables


def make_text(source, variables):
    result = "x="
    for c in source:
        number = ord(c)
        if number <= 10 or number % 10 == 0:
            variable = variables[number]
            result += 'c%' + variable
        elif c in variables:
            result += variables[c]
        else:
            variable = variables[number % 10] + '+' + variables[floor_to_tens(number)]
            result += 'c%(' + variable + ')'
        result += '+'
    result = result[:-1] + LINE_SEP  # remove last + and add line separator
    return result


def histogram(source):
    return Counter(source).most_common()


def main():
    parser = argparse.ArgumentParser('Change python code to PythonF_ck')
    parser.add_argument('file', help='File to process')
    parser.add_argument('output', help='File to save output', default='output0.py')

    class Opt:
        tabs = True

    args = parser.parse_args(namespace=Opt)
    if not os.path.isfile(args.file):
        print(f'Input file not found: {args.file}', file=sys.stderr)
    if not os.path.isfile(args.output):
        print(f'Output file not found: {args.output}', file=sys.stderr)
    source = open(args.file).read()
    tokens = token_utils.listified_tokenizer(source)
    source = minification.minify(tokens, args)
    hist = histogram(source)
    result, numbers = init_numbers(hist)
    result += make_text(source, numbers)
    result += 'exec(x)'

    open(args.output, 'w+').write(result)
    print('Done.')


if __name__ == '__main__':
    main()
