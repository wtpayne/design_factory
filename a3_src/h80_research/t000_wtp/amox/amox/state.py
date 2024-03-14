# -*- coding: utf-8 -*-
"""
---

title:
    "Amox state."

description:
    "This module defines Amox application state."

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


import asyncio
import calendar
import datetime

import pydantic
import reflex

import amox.const


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
    Amox application state.

    """

    id_user:            str              = '1a78815c-a4cb-4468-a8e6-3abecad6d4e5'
    is_ena_lightmode:   bool             = False
    is_ena_mainmenu:    bool             = False
    str_type_overlay:   str              = 'none'

    iter_str_month_nav: list[str]        =  ['January',   'February',
                                             'March',     'April',
                                             'May',       'June',
                                             'July',      'August',
                                             'September', 'October',
                                             'November',  'December']
    month_selected:     int              = datetime.date.today().month
    year_selected:      int              = datetime.date.today().year

    COUNT_IDX:          int              = 42
    list_idx_day:       list[int]        = list(range(COUNT_IDX))
    list_day_type:      list[str]        = ['inactive'] * COUNT_IDX
    list_day_of_month:  list[int]        = [0]          * COUNT_IDX
    list_str_icon:      list[list[str]]  = ['none']     * COUNT_IDX
    idx_day_selected:   int              = 0

    iter_tup_menuitem:  list[tuple[str]] = [('settings',  'Settings'),
                                            ('plus',      'New Note')]

    list_str_item:      list[str]   = ['10:00',
                                       '13:00',
                                       '15:30']
    list_str_setting:   list[str]  = ['darkmode']

    # -------------------------------------------------------------------------
    def on_click_nav_month_prev(self):
        """
        Handle the previous consecutive month being selected.

        """

        first_of_month      = datetime.datetime(self.year_selected,
                                                self.month_selected,
                                                1)
        last_of_prev_month  = first_of_month - datetime.timedelta(days = 1)
        self.month_selected = last_of_prev_month.month
        self.year_selected  = last_of_prev_month.year
        self._update_state_monthview()

    # -------------------------------------------------------------------------
    def on_select_nav_month(self, value, _):
        """
        Handle a new month being selected.

        """

        self.month_selected = datetime.datetime.strptime(value, '%B').month
        self._update_state_monthview()

    # -------------------------------------------------------------------------
    def on_select_nav_year(self, value, _):
        """
        Handle a new year being selected.

        """

        self.year_selected = int(value)
        self._update_state_monthview()

    # -------------------------------------------------------------------------
    def on_click_nav_month_next(self):
        """
        Handle the next consecutive month being selected.

        """

        first_of_month         = datetime.datetime(self.year_selected,
                                                   self.month_selected,
                                                   1)
        some_day_in_next_month = first_of_month + datetime.timedelta(days = 31)
        self.month_selected    = some_day_in_next_month.month
        self.year_selected     = some_day_in_next_month.year
        self._update_state_monthview()

    # -------------------------------------------------------------------------
    def on_click_mv_day_past(self, idx):
        """
        Handle when a past day is clicked in the monthview component.

        """

        print('PAST')

    # -------------------------------------------------------------------------
    def on_click_mv_today(self, idx):
        """
        Handle when today is clicked in the monthview component.

        """

        self.idx_day_selected = idx
        self._update_state_overlay_day()
        self.str_type_overlay = 'day'

    # -------------------------------------------------------------------------
    def on_click_mv_day_future(self, idx):
        """
        Handle when a future day is clicked in the monthview component.

        """

        print('FUTURE')

    # -------------------------------------------------------------------------
    def on_click_mainmenu(self):
        """
        """

        self.is_ena_mainmenu = not self.is_ena_mainmenu

    # -------------------------------------------------------------------------
    def on_click_mainmenu_item(self, str_item):
        """
        """

        if str_item.lower() == 'settings':
            self.on_settings_open()
        self.is_ena_mainmenu = False

    # -------------------------------------------------------------------------
    def on_click_settings_item(self, str_item):
        """
        """

        if str_item.lower() == 'darkmode':
            self.on_toggle_color_mode()

    # -------------------------------------------------------------------------
    def on_settings_open(self):
        """
        Open the settings overlay.

        """

        self.str_type_overlay = 'settings'

    # -------------------------------------------------------------------------
    def on_settings_close(self):
        """
        Close the settings overlay.

        """

        self.str_type_overlay = 'none'

    # -------------------------------------------------------------------------
    def on_click_daily_item(self, str_item):
        """
        Handle when an item is clicked in the day overlay component.

        """

        print(str_item)

    # -------------------------------------------------------------------------
    def on_toggle_overlay_day(self):
        """
        Toggle the day overlay.

        """

        if self.str_type_overlay == 'day':
            self.str_type_overlay = 'none'
        else:
            self.str_type_overlay = 'day'

    # -------------------------------------------------------------------------
    def on_toggle_color_mode(self):
        """
        Toggle lightmode and darkmode.

        """

        self.is_ena_lightmode = not self.is_ena_lightmode

    # -------------------------------------------------------------------------
    @reflex.var
    def iter_str_year_nav(self) -> list[str]:
        """
        Return an iterable over year strings for navigation.

        """

        count_year_each_way = 1
        year_start          = self.year_selected - count_year_each_way
        year_end            = self.year_selected + count_year_each_way + 1

        return [str(year) for year in range(year_start, year_end)]

    # -------------------------------------------------------------------------
    @reflex.var
    def str_year_selected(self) -> str:
        """
        Return the human readable string representation of the selected year.

        """

        return str(self.year_selected)

    # -------------------------------------------------------------------------
    @reflex.var
    def str_month_selected(self) -> str:
        """
        Return the human readable string representation of the selected month.

        """

        return calendar.month_name[self.month_selected]

    # -------------------------------------------------------------------------
    def handle_page_index_on_load(self):
        """
        Handle the on_load event on the index page.

        """

        date_today          = datetime.date.today()
        self.year_selected  = date_today.year
        self.month_selected = date_today.month
        self._update_state_monthview()

    # -------------------------------------------------------------------------
    def _update_state_monthview(self):
        """
        Update the monthview component state.

        """

        self.list_day_type     = ['inactive'] * self.COUNT_IDX
        self.list_day_of_month = [0]          * self.COUNT_IDX
        self.list_str_icon     = ['none']     * self.COUNT_IDX

        date_today             = datetime.date.today()
        is_selected_month      = (     self.year_selected  == date_today.year
                                   and self.month_selected == date_today.month)
        calendar_month         = calendar.monthcalendar(self.year_selected,
                                                        self.month_selected)
        idx = 0
        for week in calendar_month:
            for day in week:

                is_valid_day = (day != 0)

                if is_valid_day:
                    date_of_day = datetime.date(self.year_selected,
                                                self.month_selected,
                                                day)
                    is_future   = date_of_day >  date_today
                    is_past     = date_of_day <  date_today
                    is_today    = date_of_day == date_today
                else:
                    is_future   = False
                    is_past     = False
                    is_today    = False

                if not is_valid_day:
                    self.list_day_type[idx]     = 'inactive'
                    self.list_str_icon[idx]     = 'none'
                    self.list_day_of_month[idx] = 0

                elif is_past:
                    self.list_day_type[idx]     = 'past'
                    self.list_str_icon[idx]     = 'none'
                    self.list_day_of_month[idx] = day

                elif is_today:
                    self.list_day_type[idx]     = 'today'
                    self.list_str_icon[idx]     = 'smile'
                    self.list_day_of_month[idx] = day

                elif is_future:
                    self.list_day_type[idx]     = 'future'
                    self.list_str_icon[idx]     = 'none'
                    self.list_day_of_month[idx] = day

                else:
                    raise RuntimeError('Something bad went wrong.')

                idx += 1

    # -------------------------------------------------------------------------
    def _update_state_overlay_day(self):
        """
        """

        pass