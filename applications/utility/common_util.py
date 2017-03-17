#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib


def encode_passwd(uuid, passwd):
    sha1_passwd = '%s:%s' % (uuid, passwd)
    return hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest()