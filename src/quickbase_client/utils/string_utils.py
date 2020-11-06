from collections import namedtuple
import keyword
import re
import string
from urllib.parse import urlparse

import stringcase


VarMakerStrategy = namedtuple('VarMakerStrategy', 'case_func,special_replacer')

_case_map = {
    'snake': VarMakerStrategy(stringcase.snakecase, '_'),
    'pascal': VarMakerStrategy(stringcase.pascalcase, ''),
    'camel': VarMakerStrategy(stringcase.camelcase, '')  # :(
}

_number_map = {
    'drop': lambda v: v.lstrip(string.digits),
    'underscore': lambda v: f'_{v}'
}


def make_var_name(s: str, case='snake', number_strategy='drop'):
    case_func, special_replacer = _case_map[case]

    # replace special chars, and strip them from the ends
    v = re.sub(r'[\W_]+', special_replacer, s)
    v = v.strip(special_replacer)

    # force consecutive caps to not split things up
    minimizing = False
    s = ''
    for c in v:
        if c.isupper() and minimizing:
            c = c.lower()
        else:
            minimizing = c.isupper()
        s += c

    # do the actual conversion and handle leading numbers
    v = case_func(s)
    v = _number_map[number_strategy](v) if v[0].isnumeric() else v

    if v[0] == '_' and number_strategy != 'underscore':
        v = v.lstrip('_')
    v = v.replace('__', '_')  # patch for a_b_c => a__b__c

    return v + ('_' if keyword.iskeyword(v) else '')


def make_unique_var_name(s: str, taken, case='snake', number_strategy='drop'):
    var_name = make_var_name(s, case, number_strategy)
    if var_name in taken:
        for i in range(2, 1000):
            if f'{var_name}_{i}' not in taken:
                return f'{var_name}_{i}'
    return var_name


def id_from_iso_string(s):
    return s.replace(':', '')\
        .replace('T', '')\
        .replace('Z', '')\
        .replace('-', '')\
        .replace('.', '')


def parse_realm_and_app_id_from_url(url):
    url = f'https://{url}' if 'https://' not in url else url
    parsed = urlparse(url)
    return parsed.hostname, parsed.path.split('/')[-1]
