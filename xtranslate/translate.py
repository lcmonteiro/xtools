# =======================================================================================
# @autor: Luis Monteiro 
# =======================================================================================
from argparse import ArgumentError, ArgumentParser
from pathlib import Path
from pprint import pprint
from pandas import read_excel
from xml.etree.ElementTree import parse as read_xml
from re import compile, MULTILINE, DOTALL, IGNORECASE

# =======================================================================================
# settings
# =======================================================================================
IGNORE  = "\[\]\"#$%&'()*+,.\/:;<=>?@\^_`{|}~\-\d\s"
PATTERN = compile(
    f"[{IGNORE}]*([^{IGNORE}].*[^{IGNORE}])[{IGNORE}]*", MULTILINE|DOTALL|IGNORECASE)

# =======================================================================================
# helpers
# =======================================================================================
def extract_data(text):
    try:
        return str(PATTERN.match(text).group(1))
    except:
        return None


def substitute_data(origin, translated):
    return origin.replace(
        PATTERN.match(origin).group(1), 
        PATTERN.match(translated).group(1))


def load_dictionary(path):
    dictionary = {extract_data(r.iloc[0]):r.iloc[1] for _,r in read_excel(path).iterrows()}
    dictionary.pop(None, None)
    dictionary.pop('', None)
    return dictionary


def translate_xml(origin, dictionary, translated):
    tree = read_xml(origin)
    root = tree.getroot()
    for elem in root.iter():
        key = extract_data(elem.text)
        if not key:
            continue
        if key not in dictionary:
            print(f'WARNING: no translation found to : "{elem.text}"')
            continue
        elem.text = substitute_data(elem.text, dictionary[key])
    tree.write(translated, encoding='UTF-8')

def handle_io_paths(input, output, callback):
    def process_dir():
        for path in input.iterdir():
            if path.is_dir():
                continue
            callback(path, output/path.name)
    def process_error():
        raise ArgumentError("Check input and output path")
    {   # process all options 
        (True, True ) : lambda: process_dir(),
        (True, False) : lambda: process_error(),
        (False,True ) : lambda: callback(input, output/input.name),
        (False,False) : lambda: callback(input, output)
    }[(input.is_dir(), output.is_dir())]()


# =======================================================================================
# entry point
# =======================================================================================
def main(args=None):
    # parse commnand line arguments
    parser = ArgumentParser()
    parser.add_argument('--input', '-i', 
        help='input path.', type=str, required=True)
    parser.add_argument('--dictionary', '-d', 
        help='dictionary file path.', type=str, required=True)
    parser.add_argument('--output', '-o', 
        help='output path.', type=str, required=True)
    arguments = parser.parse_args(args=args)

    def try_translate_xml(input, dictionary, output):
        print()
        print(f"INFO   : Try to translate '{input}' file ...")
        try:
            translate_xml(input, dictionary, output)
        except Exception as ex:
            print(f"WARNING: {input}: {ex}")

    try:
        dictionary = load_dictionary(Path(arguments.dictionary))
        handle_io_paths(
            Path(arguments.input),
            Path(arguments.output),
            lambda input, output: try_translate_xml(input, dictionary, output))
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
   main()