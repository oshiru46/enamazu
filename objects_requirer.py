
def require_not_none(object, vname):
    if object is None:
        raise ValueError(f"Invalid value for {vname}. Expected not None, but was None.")
    pass

def require_not_empty(string, vname):
    if string == "":
        raise ValueError(f"Invalid value for {vname}. Expected not empty, but was empty.")
    pass
