# -*- coding: utf-8 -*-
"""
---

title:
    "Utility commands package."

description:
    "This package provides commands to run
    various design process utility functions."

id:
    "f94d59d0-d11e-473c-81d9-8c55edf4fd45"

type:
    dt002_python_package

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

...
"""


# -----------------------------------------------------------------------------
def uuid():
    """
    Generate a UUID and copy it to the clipboard.

    """
    import uuid
    import pyclip

    obj_uuid = uuid.uuid4()
    str_uuid = str(obj_uuid)

    pyclip.copy(str_uuid)
    print('Copied to clipboard: ' + str_uuid)

    return 0
