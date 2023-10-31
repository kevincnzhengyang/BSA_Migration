#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 21:22:51
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-11-01 00:19:09
* @FilePath    : /BSA_Migration/api/activities.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
import httpx
import time
import pandas as pd

from nicegui import app, ui
from loguru import logger

host = 'https://tmweb.troopmaster.com'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}


def get_activities_list() -> pd.DataFrame:
    with httpx.Client(headers=headers) as client:
        # get cookie for pick site
        r = client.get(host + '/Login/PickSite', headers=headers, timeout=10.0)
        r.raise_for_status()
        cookie = r.headers["set-cookie"].split(";")[0]
        logger.debug(f"cookie={cookie}")
        headers.update({"Cookie": cookie})
        # select state
        r = client.post(host + '/Login/SelectState',
                        data={"state": app.storage.general['TM_STATE']},
                        headers=headers, timeout=10.0)
        r.raise_for_status()
        logger.debug(f"tenantid={r.json()['tenantid']}")
        # select site, get cookie for session
        r = client.post(host + '/Login/SiteSelected',
                        data={"SiteId": app.storage.general['TM_SITEID']},
                        headers=headers, timeout=10.0)
        r.raise_for_status()
        cookie = cookie + "; " + r.headers["set-cookie"].split(";")[0]
        headers.update({"Cookie": cookie})
        # login
        r = client.post(host + '/Login/Login',
                        data={"UserID": app.storage.general['TM_USERID'],
                              "Password": app.storage.general['TM_PASSWORD']},
                        headers=headers, timeout=10.0)
        r.raise_for_status()
        if r.json()["message"]:
            logger.error(r.json()["message"])
            raise IOError("Failed to Login")
        for c in r.headers.get_list("set-cookie"):
            cookie = cookie + "; " + c.split(";")[0]
        cookie = cookie + "; HomeTroopMasterWebSiteID=206136"
        logger.debug(f"cookie={cookie}")
        headers.update({"Cookie": cookie})
        # ui.notify(f"Login TroopMaster Success")
        # keep alive
        # r = client.post(host + '/Home/KeepAlive', headers=headers, timeout=10.0)
        # r.raise_for_status()
        # get all activities
        r = client.post(host + '/ActivityManagement/MemberFilter/?id=all', timeout=10.0, headers=headers)
        r.raise_for_status()
        # ui.notify(f"Get all activities")
        return pd.read_json(r.text)

def get_act_details(df: pd.DataFrame) -> None:

    with httpx.Client(headers=headers) as client:
        # keep alive
        r = client.post(host + '/Home/KeepAlive', headers=headers, timeout=10.0)
        r.raise_for_status()

        # get details of an activity
        headers.update({'X-Requested-With': 'XMLHttpRequest'})

        r = client.get(host + '/ActivityManagement/View/', timeout=10.0,
                       params={"id": "206136d884d9076fa94bf09a09bfa174ffa823",
                               "_": int(time.time())},
                      headers=headers)
        r.raise_for_status()
        # print(r.text)
    return df

def export_activities(param: object) -> list:
    # get all activities
    df = get_activities_list()
    # convert datetime
    df['StartDate'] = pd.to_datetime(df['StartDateStr'], format="mixed")
    df['EndDate'] = pd.to_datetime(df['EndDateStr'], format="mixed")
    # set start date as index and truncate
    df['date'] = df['StartDate']
    df = df.set_index("date").sort_index(ascending=True)
    logger.info(f"from {param.begin} to {param.end}, {param.act_types}")
    df = df[param.begin: param.end]
    # filter with activity type
    df = df[df['Type'].isin(param.act_types)]
    # ui.notify(f"{len(df)} activities to be exported")
    logger.info(f"{len(df)} activities to be exported")
    # new column for attendances, amount, credits, remark and description
    df = df.assign(Attendances="", Amount="", Credits="", Remarks="", Description="")
    # delete columns
    df = df.drop(['Color', 'StartDateStr', 'EndDateStr', 'Register',
                  'Status', 'RegisterWithNum', 'AllDay'], axis=1)
    get_act_details(df)
    return df.astype(str).to_dict('records')

