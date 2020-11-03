from collections import namedtuple
import keyword
import re
import string

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
    v = re.sub(r'[\W_]+', special_replacer, s)
    v = case_func(v)

    v = _number_map[number_strategy](v) if v[0].isnumeric() else v

    if v[0] == '_' and number_strategy != 'underscore':
        v = v.lstrip('_')
    v = v.replace('__', '_')  # patch for a_b_c => a__b__c

    return v + ('_' if keyword.iskeyword(v) else '')


def make_unique_var_name(s: str, taken, case='snake', number_strategy='drop'):
    var_name = make_var_name(s, case, number_strategy)
    i = 2
    if var_name in taken:
        while i < 1000:
            if f'{var_name}_{i}' not in taken:
                return f'{var_name}_{i}'
    return var_name


def id_from_iso_string(s):
    return s.replace(':', '').replace('T', '').replace('-', '')
