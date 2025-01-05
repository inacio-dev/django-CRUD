import re


def camel_to_snake(name):
    s1 = re.sub("([A-Z])", r"_\1", name)
    return s1.lower().lstrip("_")


def dict_keys_camel_to_snake(data):
    if isinstance(data, dict):
        return {camel_to_snake(k): dict_keys_camel_to_snake(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [dict_keys_camel_to_snake(i) for i in data]
    else:
        return data


def snake_to_camel(name):
    components = name.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def dict_keys_snake_to_camel(data):
    if isinstance(data, dict):
        return {snake_to_camel(k): dict_keys_snake_to_camel(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [dict_keys_snake_to_camel(i) for i in data]
    else:
        return data


def get_filters(filter_class, request):
    filter_params = {}

    for field_name, filter_ in filter_class.base_filters.items():
        filter_value = request.GET.get(field_name)
        if filter_value:
            if field_name.endswith("__in"):
                filter_params[field_name] = filter_value.split(",")
            else:
                filter_params[field_name] = filter_value

    return filter_params
