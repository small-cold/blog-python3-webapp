#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging;
import os

import time
from datetime import datetime

from aiohttp import web
import asyncio

from jinja2 import Environment
from jinja2 import FileSystemLoader

import orm
from common import get_app_mod
from config import configs
from controller_base import add_route
from middleware import logger_factory, response_factory

logging.basicConfig(level=logging.INFO)


def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape=kw.get('autoescape', True),
        block_start_string=kw.get('block_start_string', '{%'),
        block_end_string=kw.get('block_end_string', '%}'),
        variable_start_string=kw.get('variable_start_string', '{{'),
        variable_end_string=kw.get('variable_end_string', '}}'),
        auto_reload=kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = []
        for app_package in configs.app_packages:
            path = os.path.join(configs.app_root_path, app_package, configs.resources.templates)

    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env


def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


def middlewares():
    middlewares = [logger_factory, response_factory]

    for app_name in configs.app_packages:
        app_mod = get_app_mod(app_name, configs.app_root_name)
        for mod_name in dir(app_mod):
            if not mod_name.startswith(configs.module_prefix.middleware):
                continue
            mod = get_app_mod(mod_name, configs.app_root_name, app_name)
            for attr in dir(mod):
                if attr.startswith('_'):
                    continue
                fn = getattr(mod, attr)
                if callable(fn):
                    name = getattr(fn, '__middleware__', None)
                    priority = getattr(fn, '__priority__', None)
                    if name and priority:
                        logging.info('add middlewars name is ',name=attr , priority= priority)
                        middlewares.append(fn)
    # TODO 排序，按照priority
    return middlewares


def add_static(app):
    for one_app in configs['app_packages']:
        one_path = os.path.join(configs.app_root_path, one_app, configs.resources.static)
        app.router.add_static('/static/', one_path)
        logging.info('add static %s => %s' % ('/static/', one_path))


def add_routes(app):
    # 加载所有app包中的 controller 中的方法
    for app_name in configs['app_packages']:
        app_mod = get_app_mod(app_name, configs['app_root_name'])
        for mod_name in dir(app_mod):
            if not mod_name.startswith(configs.module_prefix.controller):
                continue
            mod = get_app_mod(mod_name, configs.app_root_name, app_name)
            for attr in dir(mod):
                if attr.startswith('_'):
                    continue
                fn = getattr(mod, attr)
                if callable(fn):
                    method = getattr(fn, '__method__', None)
                    path = getattr(fn, '__route__', None)
                    if method and path:
                        add_route(app, fn)


async def init(loop, configs=configs):
    # 创建数据库连接
    await orm.create_pool(loop=loop, **configs.db)
    # 创建应用
    app = web.Application(loop=loop, middlewares=middlewares())
    # 设置url处理函数
    add_routes(app)
    # 初始化模板引擎
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    # 添加静态资源
    add_static(app)
    # 创建服务
    srv = await loop.create_server(app.make_handler(), configs.server.host, configs.server.port)
    logging.info('server started at ' + str(configs.server))
    return srv


def start():
    # 创建应用实例,并一直运行
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    start()
