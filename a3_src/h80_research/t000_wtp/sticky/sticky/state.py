# -*- coding: utf-8 -*-
"""
---

title:
    "Sticky state."

description:
    "This module defines sticky application state."

id:
    "0f93f463-83b8-4a38-a7d5-17a98564c516"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."


"""


import calendar
import datetime

import asyncio

import pydantic
import reflex


# =============================================================================
class DayInfo(pydantic.BaseModel):
    """
    """
    do_render:    bool = False
    has_icon:     bool = True
    day_of_month: int


# =============================================================================
class App(reflex.State):
    """
    Sticky application state.

    """

    COUNT_IDX:         int        = 42
    list_idx_day:      list[int]  = list(range(COUNT_IDX))
    list_do_render:    list[bool] = [False] * COUNT_IDX
    list_day_of_month: list[int]  = [0]     * COUNT_IDX
    list_has_icon:     list[bool] = [False] * COUNT_IDX
    view_month:        int        = 0
    view_year:         int        = 0

    # -------------------------------------------------------------------------
    @reflex.var
    def view_month_name(self) -> str:
        """
        """

        return calendar.month_name[self.view_month]

    # -------------------------------------------------------------------------
    def on_click_month(self, idx):
        """
        """

        self.list_has_icon[idx] = not self.list_has_icon[idx]

    # -------------------------------------------------------------------------
    def on_click_nav_month_prev(self):
        """
        """

        first_of_month     = datetime.datetime(self.view_year,
                                               self.view_month,
                                               1)
        last_of_prev_month = first_of_month - datetime.timedelta(days = 1)
        self.view_month    = last_of_prev_month.month
        self.view_year     = last_of_prev_month.year
        self._update_calendar()

    # -------------------------------------------------------------------------
    def on_click_nav_month_next(self):
        """
        """

        first_of_month      = datetime.datetime(self.view_year,
                                                self.view_month,
                                                1)
        first_of_next_month = first_of_month + datetime.timedelta(days = 31)
        self.view_month     = first_of_next_month.month
        self.view_year      = first_of_next_month.year
        self._update_calendar()

    # -------------------------------------------------------------------------
    def handle_page_index_on_load(self):
        """
        Handle the on_load event on the index page.

        """

        date_today      = datetime.date.today()
        self.view_year  = date_today.year
        self.view_month = date_today.month
        self._update_calendar()

    # -------------------------------------------------------------------------
    def _update_calendar(self):
        """
        """

        self.list_do_render    = [False] * self.COUNT_IDX
        self.list_day_of_month = [0]     * self.COUNT_IDX
        self.list_has_icon     = [False] * self.COUNT_IDX

        idx = 0
        for week in calendar.monthcalendar(self.view_year, self.view_month):
            for day in week:
                if day != 0:
                    self.list_do_render[idx]    = True
                    self.list_has_icon[idx]     = False
                    self.list_day_of_month[idx] = day
                else:
                    self.list_do_render[idx]    = False
                    self.list_has_icon[idx]     = False
                    self.list_day_of_month[idx] = 0
                idx += 1
