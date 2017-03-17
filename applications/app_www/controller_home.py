#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from controller_base import get, post


@get("/")
def index():
    return {
        '__template__': 'index.html',
        'page': 0
    }

