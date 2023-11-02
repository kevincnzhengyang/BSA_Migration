#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 21:22:51
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-11-02 15:42:41
* @FilePath    : /BSA_Migration/api/activities.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
import httpx
import time
import pandas as pd

from pathlib import Path
from nicegui import app
from lxml import etree
from loguru import logger

host = 'https://tmweb.troopmaster.com'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}

type_amount_map = {
    "Activity": "Amount",
    "Adventure": "Amount",
    "Aquatics": "Hours",
    "Backpacking": "Nights",
    "Camping": "Nights",
    "Conservation": "Hours",
    "Court Of Honor": "Amount",
    "Cycling": "Amount",
    "Egl Ct of Honor": "Amount",
    "Fundraising": "Hours",
    "Hiking": "Miles",
    "ISB Calendar": "Amount",
    "Kayaking": "Amount",
    "Meeting": "Amount",
    "Riding": "Miles",
    "Serv Proj": "Hours",
    "Swimming": "Miles",
}

async def get_activities_list() -> pd.DataFrame:
    async with httpx.AsyncClient(headers=headers) as client:
        # get cookie for pick site
        r = await client.get(host + '/Login/PickSite', headers=headers, timeout=10.0)
        r.raise_for_status()
        cookie = r.headers["set-cookie"].split(";")[0]
        logger.debug(f"cookie={cookie}")
        headers.update({"Cookie": cookie})
        # select state
        r = await client.post(host + '/Login/SelectState',
                        data={"state": app.storage.general['TM_STATE']},
                        headers=headers, timeout=10.0)
        r.raise_for_status()
        logger.debug(f"tenantid={r.json()['tenantid']}")
        # select site, get cookie for session
        r = await client.post(host + '/Login/SiteSelected',
                        data={"SiteId": app.storage.general['TM_SITEID']},
                        headers=headers, timeout=10.0)
        r.raise_for_status()
        cookie = cookie + "; " + r.headers["set-cookie"].split(";")[0]
        headers.update({"Cookie": cookie})
        # login
        r = await client.post(host + '/Login/Login',
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
        # keep alive
        r = await client.post(host + '/Home/KeepAlive', headers=headers, timeout=10.0)
        r.raise_for_status()
        # get all activities
        r = await client.post(host + '/ActivityManagement/MemberFilter/?id=all', timeout=10.0, headers=headers)
        r.raise_for_status()
        return pd.read_json(r.text)

async def get_act_details(act_id: str) -> list:
    async with httpx.AsyncClient(headers=headers) as client:
        act_attrs = {
            "scouts": [],
            "adults": [],
        }

        # keep alive
        r = await client.post(host + '/Home/KeepAlive', headers=headers, timeout=10.0)
        r.raise_for_status()

        # get details of an activity
        headers.update({'X-Requested-With': 'XMLHttpRequest'})
        r = await client.get(host + '/ActivityManagement/View/', timeout=10.0,
                       params={"id": act_id, "_": int(time.time())},
                      headers=headers)
        r.raise_for_status()

        # parse html response
        html = etree.HTML(r.text)
        # get basic info
        for t in html.xpath('//div[@id="Activity"]/div/div')[0].iterchildren():
            if t.tag == 'b' and t.tail and t.tail.strip():
                logger.debug(f"{t.text}:{t.tail}")
                act_attrs[t.text.strip().strip(":")] = t.tail.strip()
        for t in html.xpath('//div[@id="Activity"]/div/div')[1].iterchildren():
            if t.tag == 'b':
                logger.debug(f"{t.text}:{t.tail}")
                act_attrs[t.text.strip().strip(":")] = t.tail.strip()
            elif t.tag == 'label':
                # join multiple lines into a string
                # Remarks, Documents and Description
                value = []
                for s in t.itersiblings():
                    if s.tag == 'br' and s.tail and s.tail.strip():
                        value.append(s.tail.strip())
                logger.debug(f"{t.text}:{value}")
                act_attrs[t.text.strip()] = ' '.join(value)
        # get scout attendance
        s_att = html.xpath('//div[@id="Attendance"]//td[contains(@class, "scout")]')
        for i in range(0, len(s_att), 7):
            a = s_att[i]
            child = s_att[i+1].getchildren()[0]
            if child.tag == 'span' and child.text and child.text == 'X':
                # logger.debug(f"{a.text.strip()}---1")
                act_attrs["scouts"].append(a.text.strip())
            # else:
            #     logger.debug(f"{a.text.strip()}---0")
        # get adult attendance
        a_att = html.xpath('//div[@id="Attendance"]//td[contains(@class, "scout")]')
        for i in range(0, len(a_att), 7):
            a = a_att[i]
            child = a_att[i+1].getchildren()[0]
            if child.tag == 'span' and child.text and child.text == 'X':
                # logger.debug(f"{a.text.strip()}---1")
                act_attrs["adults"].append(a.text.strip())
            # else:
            #     logger.debug(f"{a.text.strip()}---0")
        # get registration
        regs = html.xpath('//div[@id="Registration"]/div/div')
        if regs:
            for t in regs[0].iterchildren():
                if t.tag == 'b' and t.tail and t.tail.strip():
                    logger.debug(f"{t.text}:{t.tail}")
                    act_attrs[t.text.strip().strip(":")] = t.tail.strip()

        # logger.info(f"attrs={act_attrs}")
    return ["; ".join(act_attrs["scouts"]),
            "; ".join(act_attrs["adults"]),
            act_attrs.get(type_amount_map[act_attrs["Activity Type"]], ""),
            act_attrs.get("Credit Towards", ""),
            act_attrs.get("Remarks", ""),
            act_attrs.get("Documents", ""),
            act_attrs.get("Description", ""),
            act_attrs.get("Scouts Registered", "0"),
            act_attrs.get("Adults Registered", "0")]

async def complete_acts(df: pd.DataFrame) -> None:
    total = len(df)
    i = 0
    for index, row in df.iterrows():
        logger.debug(f"processing act [{row['Title']}]...")
        df.at[index, "ScoutAttendances"], df.at[index, "AdultAttendances"], \
        df.at[index, "Amount"], df.at[index, "Credits"], \
        df.at[index, "Remarks"], df.at[index, "Documents"], \
        df.at[index, "Description"], df.at[index, "ScoutsReg"], \
        df.at[index, "AdultsReg"] = await get_act_details(row["ActivityID"])
        i = i + 1
        logger.info(f"--- {i} of {total} - row['Title'] ---")
    # print(df.to_dict())
    return

def load_activities() -> list:
    # using local data
    path = Path.cwd().joinpath('acts_list.csv')
    if path.exists():
        return pd.read_csv(path).to_dict('records')
    else:
        return []

async def export_activities(param: object) -> list:
    # get all activities
    df = await get_activities_list()
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
    df = df.assign(ScoutAttendances="", AdultAttendances="", Amount="",
                   Credits="", Remarks="", Documents="", Description="",
                   ScoutsReg="", AdultsReg="")
    # delete columns
    df = df.drop(['Color', 'StartDateStr', 'EndDateStr', 'Register',
                  'Status', 'RegisterWithNum', 'AllDay'], axis=1)
    await complete_acts(df)
    # save to local
    df.to_csv(Path.cwd().joinpath('acts_list.csv'))
    return df.astype(str).to_dict('records')

