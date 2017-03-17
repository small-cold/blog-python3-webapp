#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import config_default
from common import get_mod


class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def merge(defaults, override):
    r = {}
    for k, v in defaults.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def toDict(d):
    D = Dict()
    for k, v in d.items():
        D[k] = toDict(v) if isinstance(v, dict) else v
    return D

def init(defalts):
    # 是否指定了 app_packages 的名称
    if not defalts.__contains__("app_packages"):
        app_root_name = defalts['app_root_name']
        n = app_root_name.rfind('.')
        if n == (-1):
            mod = __import__(app_root_name, globals(), locals())
        else:
            name = app_root_name[n + 1:]
            mod = getattr(__import__(app_root_name[:n], globals(), locals(), [name]), name)
        app_packages = []
        for app_package_str in dir(mod):
            if not app_package_str.startswith(defalts['app_prefix']):
                continue
            app_packages.append(app_package_str)
        defalts['app_packages'] = app_packages
    path = getattr(get_mod(defalts['app_root_name']), '__file__');
    defalts['app_root_path'] = os.path.dirname(os.path.abspath(getattr(get_mod(defalts['app_root_name']), '__file__')))
    return toDict(defalts)

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = init(configs)
