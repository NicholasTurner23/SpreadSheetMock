from dateutil.parser import parse

def check_spec(type_:str, spec:str) -> bool:
    if type_ == "number":
        if spec.startswith("%") and spec.endswith("f"):
            return True
        else:
            raise ValueError
        
    if type_ == "date":
            if spec.startswith("%"):
                return True
            else:
                raise ValueError
    return False


def formatted_value(type_, value, spec):
    if type_ == "date":
        try:
            date_ = parse(value)
            value_ = date_.strftime(spec)
        except ValueError as e:
            raise e
    elif type_ == "number":
        try:
            value_ = spec%value
        except ValueError as e:
            raise e
    else:
        raise ValueError
    return value_