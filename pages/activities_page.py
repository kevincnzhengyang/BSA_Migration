#-*-coding:UTF-8-*-


'''
* @Author      : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @Date        : 2023-10-31 19:15:28
* @LastEditors : kevin.z.y <kevin.cn.zhengyang@gmail.com>
* @LastEditTime: 2023-11-01 00:08:21
* @FilePath    : /BSA_Migration/pages/activities_page.py
* @Description :
* @Copyright (c) 2023 by Zheng, Yang, All Rights Reserved.
'''
from nicegui import ui

from pages.theme import page_frame
from api.activities import export_activities

class ActParams:
    def __init__(self):
        self.begin = "2019-1-1"
        self.end   = "2023-7-31"
        self.act_types = []
        self.activity = False
        self.adventure = False
        self.aquatics = False
        self.backpacking = False
        self.camping = False
        self.conservation = False
        self.courtofhonor = False
        self.cycling = False
        self.elg = False
        self.fundraising = False
        self.hiking = False
        self.isbcalendar = False
        self.kayaking = False
        self.meeting = False
        self.riding = False
        self.serv = False
        self.swimming = False

act_params = ActParams()


def create() -> None:
    @ui.page('/activities')
    def page_activities():
        with page_frame('Activities Migration'):
            ui.label('Activities').classes('text-h6 font-bold')
            with ui.input('From') as date:
                with date.add_slot('append'):
                    ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
                with ui.menu() as menu:
                    ui.date().bind_value(date)
                date.bind_value(act_params, "begin")
        with ui.input('To') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').on('click', lambda: menu.open()).classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)
            date.bind_value(act_params, "end")
        ui.label('Activity Type').classes('text-h9 font-bold')
        with ui.grid(columns=4):
            ui.checkbox('Activity').bind_value(act_params, "activity")
            ui.checkbox('Adventure').bind_value(act_params, "adventure")
            ui.checkbox('Aquatics').bind_value(act_params, "aquatics")
            ui.checkbox('Backpacking').bind_value(act_params, "backpacking")
            ui.checkbox('Camping').bind_value(act_params, "camping")
            ui.checkbox('Conservation').bind_value(act_params, "conservation")
            ui.checkbox('Court of Honor').bind_value(act_params, "courtofhonor")
            ui.checkbox('Cycling').bind_value(act_params, "cycling")
            ui.checkbox('Elg Ct of Honor').bind_value(act_params, "elg")
            ui.checkbox('Fundraising').bind_value(act_params, "fundraising")
            ui.checkbox('Hiking').bind_value(act_params, "hiking")
            ui.checkbox('ISB Calender').bind_value(act_params, "isbcalendar")
            ui.checkbox('Kayaking').bind_value(act_params, "kayaking")
            ui.checkbox('Meeting').bind_value(act_params, "meeting")
            ui.checkbox('Riding').bind_value(act_params, "riding")
            ui.checkbox('Serv Proj').bind_value(act_params, "serv")
            ui.checkbox('Swimming').bind_value(act_params, "swimming")

        def export_acts():
            act_params.act_types = []
            if (act_params.activity):
                act_params.act_types.append("Activity")
            if (act_params.adventure):
                act_params.act_types.append("Adventure")
            if (act_params.aquatics):
                act_params.act_types.append("Aquatics")
            if (act_params.backpacking):
                act_params.act_types.append("Backpacking")
            if (act_params.camping):
                act_params.act_types.append("Camping")
            if (act_params.conservation):
                act_params.act_types.append("Conservation")
            if (act_params.courtofhonor):
                act_params.act_types.append("Court of Honor")
            if (act_params.cycling):
                act_params.act_types.append("Cycling")
            if (act_params.elg):
                act_params.act_types.append("Elg Ct of Honor")
            if (act_params.fundraising):
                act_params.act_types.append("Fundraising")
            if (act_params.hiking):
                act_params.act_types.append("Hiking")
            if (act_params.isbcalendar):
                act_params.act_types.append("ISB Calender")
            if (act_params.kayaking):
                act_params.act_types.append("Kayaking")
            if (act_params.meeting):
                act_params.act_types.append("Meeting")
            if (act_params.riding):
                act_params.act_types.append("Riding")
            if (act_params.serv):
                act_params.act_types.append("Serv Proj")
            if (act_params.swimming):
                act_params.act_types.append("Swimming")
            grid.options['rowData'] = export_activities(act_params)
            print(grid.options['rowData'])
            grid.update()

        def import_acts():
            grid.options['rowData'] = []
            grid.update()

        def clear_grid():
            grid.options['rowData'] = []
            grid.update()

        with ui.row():
            ui.button('Export', on_click=export_acts)
            ui.button('Import', on_click=import_acts)
            ui.button('Clear', on_click=clear_grid)
        grid = ui.aggrid({
            'defaultColDef': {'flex': 1},
            'columnDefs': [
                {'headerName': 'Type', 'field': 'Type'},
                {'headerName': 'Title', 'field': 'Title'},
                {'headerName': 'Level', 'field': 'Level'},
                {'headerName': 'Start Date', 'field': 'StartDate'},
                {'headerName': 'End Date', 'field': 'EndDate'},
                {'headerName': 'Attendance Num', 'field': 'AttendanceNum'},
                {'headerName': 'Activity ID', 'field': 'ActivityID', 'hide': True},
                {'headerName': 'Attendances', 'field': 'Attendances', 'hide': True},
                {'headerName': 'Amount', 'field': 'Amount', 'hide': True},
                {'headerName': 'Credits', 'field': 'Credits', 'hide': True},
                {'headerName': 'Remark', 'field': 'Remark', 'hide': True},
                {'headerName': 'Description', 'field': 'Description', 'hide': True},
            ],
            'rowData': [],
            'rowSelection': 'multiple',
        }).classes('max-h-40')
