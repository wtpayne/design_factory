#!/usr/bin/env bash
# ---
#
# title:
#     "Embedded interactive bash shell init script."
#
# description:
#     "This script is used to initialize the
#     embedded interactive bash shell that can
#     be launched from the main design automation
#     shell script."
#
# id:
#     "ae92a21e-c660-4c6f-a767-8f872aa3dce3"
#
# type:
#     dt000_bash_script
#
# validation_level:
#     v00_minimum
#
# protection:
#     k00_general
#
# copyright:
#     "Copyright 2023 William Payne"
#
# license:
#     "Licensed under the Apache License, Version
#     2.0 (the License); you may not use this file
#     except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed
#     to in writing, software distributed under
#     the License is distributed on an AS IS BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#     either express or implied. See the License
#     for the specific language governing
#     permissions and limitations under the
#     License."
#
# ...


PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$"
PS1="(`basename \"$VIRTUAL_ENV\"`) ${PS1:-}"
export PS1
