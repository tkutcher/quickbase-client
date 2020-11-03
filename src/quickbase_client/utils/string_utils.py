import re
import string
from collections import namedtuple

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
    if s.upper() == s:
        s = s.lower()  # patch to avoid ABC => a_b_c for snake case.
    case_func, special_replacer = _case_map[case]
    v = re.sub('[\W_]+', special_replacer, s)
    v = case_func(v)
    return _number_map[number_strategy](v) if v[0].isnumeric() else v


def id_from_iso_string(s):
    return s.replace(':', '').replace('T', '').replace('-', '')
