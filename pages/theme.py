#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 18:55:02
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-10-31 19:44:31
* @FilePath    : /BSA_Migration/pages/theme.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
from contextlib import contextmanager

from nicegui import ui


@contextmanager
def page_frame(navtitle: str):
    '''Custom page frame to share the same styling and behavior across all pages'''
    ui.colors(primary='#6E93D6', secondary='#53B689', accent='#111B1E', positive='#53B689')
    with ui.header().classes('justify-between text-white'):
        ui.label(navtitle).classes('font-bold')
        with ui.row():
            ui.link('Config', '/').classes(replace='text-white')
            ui.link('Scouts', '/scouts').classes(replace='text-white')
            ui.link('Activities', '/activities').classes(replace='text-white')
    # with ui.column().classes('absolute-center items-center'):
    with ui.column():
        yield
