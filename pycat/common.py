#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_mod(module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    return mod


def get_app_mod(module_name, *packages):
    if not packages:
        mod = __import__(module_name, globals(), locals())
    else:
        package_name = packages[0]
        if len(packages) > 1:
            for package in packages[1:]:
                package_name += '.' + package
        mod = getattr(__import__(package_name, globals(), locals(), [module_name]), module_name)
    return mod


if __name__ == '__main__':
    module_name = "applications.app_www.controller_home"
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        package_name = module_name[:n]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)

    print("jieshu")