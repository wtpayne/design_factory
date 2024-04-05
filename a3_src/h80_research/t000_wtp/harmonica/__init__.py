# -*- coding: utf-8 -*-
"""
---

title:
    "Harmonica package."

description:
    "This package contains functionality for
    the Harmonica system."

id:
    "831dad01-9128-46bd-ad29-293851d815d8"

type:
    dt002_python_package

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2024 William Payne"

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


import importlib.metadata


name_app     = 'Harmonica'
name_package = f't000_wtp.{name_app.lower()}'
try:
    __version__ = importlib.metadata.version(name_package)
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'
