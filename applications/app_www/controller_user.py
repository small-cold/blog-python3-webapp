#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import json
import time

from aiohttp import web

from .const import COOKIE_NAME, _COOKIE_KEY
from applications.utility.common_util import encode_passwd
from applications.utility.db_util import next_id
from .models import User
from applications.utility.valid_util import is_email, is_sha1, is_verify_code
from controller_base import get, post
from pycat import APIValueError, APIError

@get("/login")
async def login():
    return {
        '__template__': '/user/login.html',
    }


@post("/api/authenticate")
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', '邮箱不能为空.')
    if not passwd:
        raise APIValueError('passwd', '密码不能为空.')

    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('login_error', '邮箱或密码错误.')
    user = users[0]
    # 校验密码，OHTER ：密码和用户名一起查询
    cur_passwd = encode_passwd(user.id, passwd)
    if user.passwd != cur_passwd:
        raise APIValueError('login_error', '邮箱或密码错误.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get("/register")
async def register():
    return {
        '__template__': '/user/register.html',
    }

@post("/api/user/create")
async def create_user(*, name, email, passwd, code):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not is_email(email):
        raise APIValueError('email')
    if not passwd or not is_sha1(passwd):
        raise APIValueError('passwd')
    if not code or not is_verify_code(code):
        raise APIValueError('code')

    # 检查邮箱是否存在
    users =  await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')

    # TODO 检查验证码是否存在，与邮箱是否匹配
    uuid = next_id()
    image = 'http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest()
    new_user = User(id=uuid, name=name, email=email, passwd=encode_passwd(uuid, passwd), image='/static/default_photo.png')
    await new_user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(new_user, 86400), max_age=86400, httponly=True)
    new_user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(new_user, ensure_ascii=False).encode('utf-8')
    return r

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)