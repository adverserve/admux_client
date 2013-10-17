# coding: utf-8

def _list(values):
    if values:
        values = ",".join(values)
    return values

def _in_list(value, restricted_to):
    if value and value not in restricted_to:
        raise ValueError("Value (%s) not in range ([ %s ])" % \
                         (value,
                          ", ".join(restricted_to)))
    return value

def _int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

def _bool(val):
    if val:
        return 1
    return None

def _datetime(val):
    """ Format: u"2013-10-05T20:15:00" """
    if val:
        return val.strftime(u"%Y-%m-%dT%H:%M:%S")
    return None

def _clean_dict(dictionary):
    return dict(
        filter(lambda x: x[1] is not None, dictionary.items())
    )
