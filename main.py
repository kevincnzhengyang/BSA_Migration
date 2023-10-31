#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 12:55:11
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-10-31 20:38:05
* @FilePath    : /BSA_Migration/main.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''

from loguru import logger
from nicegui import app, ui

import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

import pages.config_page as config_page
import pages.scouts_page as scouts_page
import pages.activities_page as activities_page

# config logger
logger.add("run.log", rotation="50 MB", retention="7 days", compression="zip")

def load_env():
    # load env variables
    logger.info(f"Load Env Variables")
    load_dotenv(find_dotenv(Path.cwd().joinpath('config.env')))
    app.storage.general['TM_USERID'] = os.getenv('TM_USERID')
    app.storage.general['TM_PASSWORD'] = os.getenv('TM_PASSWORD')
    app.storage.general['TM_STATE'] = os.getenv('TM_STATE')
    app.storage.general['TM_SITEID'] = os.getenv('TM_SITEID')
    app.storage.general['SB_USERID'] = os.getenv('SB_USERID')
    app.storage.general['SB_PASSWORD'] = os.getenv('SB_PASSWORD')

app.on_startup(load_env)

# create web pages
config_page.create()
scouts_page.create()
activities_page.create()

ui.run(title="BSA Troop 701 Data Migration")
