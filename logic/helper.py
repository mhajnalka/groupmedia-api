import inspect
from datetime import date


def fill_data(classname, json):
    request_data = json
    for i in inspect.getmembers(classname):
        key = str(i[0])
        if not key.startswith('_') and not key.startswith('ref_') and key not in request_data.keys():
            request_data[key] = ""
    return request_data


def value_chk(request_data, *args):
    for arg in args.keys():
        if (isinstance(request_data[arg], int) and request_data[arg] is 0) or (
                isinstance(request_data[arg], str) and request_data[arg] is "") or \
                (isinstance(request_data[arg], date) and request_data[arg] is ""):
            return f"{args[arg].capitalize()} must be given."
    return ""
