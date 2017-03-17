#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
_RE_VERIFY_CODE = re.compile(r'^[0-9]{6}$')

def is_email(email):
    return _RE_EMAIL.match(email)

def is_sha1(sha1_str):
    return _RE_SHA1.match(sha1_str)

def is_verify_code(code):
    return _RE_VERIFY_CODE.match(code)