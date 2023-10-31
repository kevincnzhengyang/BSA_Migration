#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 19:04:36
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-10-31 20:38:01
* @FilePath    : /BSA_Migration/pages/config_page.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
from nicegui import app, ui
from loguru import logger

import os
from dotenv import set_key, find_dotenv
from pathlib import Path

from pages.theme import page_frame

def save_env(key: str, value: str) -> None:
    # save .env file
    set_key(find_dotenv(Path.cwd().joinpath('config.env')),
            key_to_set=key,
            value_to_set=value)
    # update storage
    app.storage.general[key] = value
    logger.info(f"set {key} to {value}")
    ui.notify(f"set {key} to {value}")

def create() -> None:
    @ui.page('/')
    def page_config():
        with page_frame('Parameter Config'):
            ui.label('Parameters for TroopMaster.').classes('text-h6 font-bold')
            tm_userid = ui.input(label='User ID',
                                 placeholder='start typing',
                                 value=app.storage.general['TM_USERID']
                                 ).on('keydown.enter',
                                      lambda: save_env('TM_USERID',
                                                       tm_userid.value))
            tm_passwd = ui.input(label='Password',
                                 placeholder='start typing',
                                 value=app.storage.general['TM_PASSWORD']
                                 ).on('keydown.enter',
                                      lambda: save_env('TM_PASSWORD',
                                                       tm_passwd.value))
            tm_state = ui.input(label='State',
                                placeholder='start typing',
                                value=app.storage.general['TM_STATE']
                                ).on('keydown.enter',
                                     lambda: save_env('TM_STATE',
                                                      tm_state.value))
            tm_siteid = ui.input(label='Site ID',
                                 placeholder='start typing',
                                 value=app.storage.general['TM_SITEID']
                                 ).on('keydown.enter',
                                      lambda: save_env('TM_SITEID',
                                                       tm_siteid.value))
            ui.label('Parameters for ScoutingBook.').classes('text-h6 font-bold')
            sb_userid = ui.input(label='User ID',
                                 placeholder='start typing',
                                 value=app.storage.general['SB_USERID']
                                 ).on('keydown.enter',
                                      lambda: save_env('SB_USERID',
                                                       sb_userid.value))
            sb_passwd = ui.input(label='Password',
                                 placeholder='start typing',
                                 value=app.storage.general['SB_PASSWORD']
                                 ).on('keydown.enter',
                                      lambda: save_env('SB_PASSWORD',
                                                       sb_passwd.value))
