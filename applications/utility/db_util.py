#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

import time


def next_id():
    """ get uuid as id """
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)