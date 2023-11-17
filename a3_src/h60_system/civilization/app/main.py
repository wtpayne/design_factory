#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
---

title:
    "Civilization app."

description:
    "Civilization app."

id:
    "7b5c9773-1f8e-4c31-b6a3-43c88aec66a8"

type:
    dt001_python_script

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


import jnius
import kivy
import kivy.app
import kivy.core.audio
import kivy.uix.boxlayout
import kivy.uix.button
import kivy.uix.label


# =============================================================================
class Civilization(kivy.app.App):
    """
    """

    # -------------------------------------------------------------------------
    def _request_permissions(self):
        """
        """

        if kivy.platform == "android":

            import android.permissions
            permit = android.permissions.Permission
            android.permissions.request_permissions([
                                            permit.INTERNET,
                                            permit.CAMERA,
                                            permit.RECORD_AUDIO,
                                            permit.WRITE_EXTERNAL_STORAGE,
                                            permit.READ_EXTERNAL_STORAGE])

    # -------------------------------------------------------------------------
    def _start_audio_recorder(self):
        """
        """

        if kivy.platform == "android":

            self._stop_audio_recorder()

            ac           = jnius.autoclass
            Recorder     = ac('android.media.MediaRecorder')
            AudioSource  = ac('android.media.MediaRecorder$AudioSource')
            OutputFormat = ac('android.media.MediaRecorder$OutputFormat')
            AudioEncoder = ac('android.media.MediaRecorder$AudioEncoder')
            File         = ac('java.io.File')
            PyActivity   = ac('org.kivy.android.PythonActivity')
            Activity     = PyActivity.mActivity
            cachedir     = Activity.getCacheDir()
            tmpfile      = File.createTempFile('audio', '.ogg', cachedir)

            self.filepath_tmp = tmpfile.getAbsolutePath()

            self.rec = Recorder()
            self.rec.setAudioSource(AudioSource.MIC)
            self.rec.setOutputFormat(OutputFormat.OGG)
            self.rec.setAudioEncoder(AudioEncoder.OPUS)
            self.rec.setOutputFile(tmpfile)
            self.rec.prepare()
            self.rec.start()

    # -------------------------------------------------------------------------
    def _stop_audio_recorder(self):
        """
        """

        if kivy.platform == "android":

            if self.rec is not None:

                self.rec.stop()
                self.rec.release()
                self.rec = None

    # -------------------------------------------------------------------------
    def _play_media(self,filepath):
        """
        """

        if kivy.platform == "android":

            ac                = jnius.autoclass
            MediaPlayer       = ac('android.media.MediaPlayer')
            File              = ac('java.io.File')
            FileDescriptor    = ac('java.io.FileDescriptor')
            media_player      = MediaPlayer()
            audio_file        = File(filepath)
            file_descriptor   = FileDescriptor()
            file_input_stream = audio_file.getAbsolutePath()
            media_player.setDataSource(file_input_stream)
            media_player.prepare()
            media_player.start()

    # -------------------------------------------------------------------------
    def build(self):
        """
        """

        self._request_permissions()
        self.rec = None

        self.root  = kivy.uix.boxlayout.BoxLayout(orientation = 'vertical')
        self.label = kivy.uix.label.Label(text = 'Press the button and speak')
        self.root.add_widget(self.label)

        self.button = kivy.uix.button.Button(text = 'Press to Speak')
        self.button.bind(on_press   = self.start_recording,
                         on_release = self.stop_recording)
        self.root.add_widget(self.button)

        return self.root

    # -------------------------------------------------------------------------
    def start_recording(self, *args):
        """
        """

        self.label.text = 'Listening...'
        self._start_audio_recorder()

    # -------------------------------------------------------------------------
    def stop_recording(self, *args):
        """
        """

        self.label.text = 'Press the button and speak'
        self._stop_audio_recorder()
        self.process_audio()

    # -------------------------------------------------------------------------
    def process_audio(self):
        """
        """

        self._play_media(self.filepath_tmp)


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    Civilization().run()
