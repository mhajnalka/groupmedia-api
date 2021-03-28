import inspect


def fill_data(classname, json):
    request_data = json
    for i in inspect.getmembers(classname):
        key = str(i[0])
        if not key.startswith('_') and not key.startswith('ref_') and key not in request_data.keys():
            request_data[key] = ""
    return request_data
