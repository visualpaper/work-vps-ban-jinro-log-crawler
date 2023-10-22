import os

THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def mockdata(path):
    test_data_path = os.path.normpath(os.path.join(THIS_SCRIPT_DIR, './data/' + path))

    with open(test_data_path, "r", encoding='utf-8') as f:
        return f.read()
