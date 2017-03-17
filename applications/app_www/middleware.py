#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from aiohttp import web

from middleware import middleware
from .models import cookie2user
from .const import COOKIE_NAME


@middleware(name='auth_factory', priority=10)
async def auth_factory(app, handler):
    async def auth(request):
        # logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                # logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or request.__user__.kind != 1):
            # 如果不是管理员或非登录状态，返回找不到连接
            return web.HTTPNotFound()
        return (await handler(request))
    return auth