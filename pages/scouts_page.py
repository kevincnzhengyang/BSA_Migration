#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 19:10:33
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-10-31 20:40:07
* @FilePath    : /BSA_Migration/pages/scouts_page.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
from nicegui import ui

from pages.theme import page_frame

def create() -> None:
    @ui.page('/scouts')
    def page_scouts():
        with page_frame('Scouts Migration'):
            ui.label('Scouts').classes('text-h6 font-bold')
