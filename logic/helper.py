import inspect
from datetime import date


# This function fills the key-value pairs of request_data, so that all keys will be properly defined
def fill_data(classname, json, orig_data):
    request_data = json
    for i in inspect.getmembers(classname):
        key = str(i[0])
        if not key.startswith('_') and not key.startswith('ref_') and key not in request_data.keys():
            if orig_data:
                request_data[key] = orig_data[key]
            else:
                request_data[key] = ""
    return request_data


# This function checks if passed arguments of request can be nullable, returns error  message if not
def value_chk(request_data, *args):
    for arg in args.keys():
        if (isinstance(request_data[arg], int) and request_data[arg] is 0) or (
                isinstance(request_data[arg], str) and request_data[arg] is "") or \
                (isinstance(request_data[arg], date) and request_data[arg] is ""):
            return f"{args[arg].capitalize()} must be given."
    return ""
