#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Configuration
'''
import os

__author__ = 'Jerry Wang'

configs = {
    'app_root_name':'applications',
    'app_prefix':'app',
    'debug': True,
    'server': {
        'host': '127.0.0.1',
        'port': 9000,
    },
    'module_prefix': {
        'controller':'controller',
        'middleware':'middleware',
        'model':'model'
    },
    'resources':{
        'static':'static',
        'templates': 'templates'
    },
    'session': {
        'secret': 'sunday'
    },
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db_name': 'sunday'
    },
}