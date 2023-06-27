======================
Creating a Discord Bot
======================

This process provides guidance on how to set up
a new instance of the Accord discord bot.

.. contents:: Table of Contents
   :local:


Creating a discord bot account
==============================

Before writing code for the bot, you need to
create a bot account from the Discord developer
portal.

#. Go to the Discord Developer Portal
   (https://discord.com/developers/applications)
#. Click on the "New Application" button.
#. Give a name to the application and click on
   "Create".
#. Click on the "Bot" tab and then click
   "Add Bot". Confirm the popup.
#. Copy the token under the "Bot" tab and
   keep it somewhere safe. If you lose it
   you can generate a new one by clicking
   on ``Reset Token``


Configuring the discord bot
===========================

In the "Bot" tab, make sure the following are
selected by clicking the grey button on the right
(blue means selected)::

  * PUBLIC BOT
  * PRESENCE INTENT
  * SERVER MEMBERS INTENT
  * MESSAGE CONTENT INTENT

Now save the changes made to the Bot tab.


Inviting the bot to a server
============================

To interact with your bot, it needs to be added
to a server.

#. Open the 'OAuth2' tab, then click on the
   'URL Generator'
#. Under ``SCOPES`` click 'bot'
#. Under 'Bot Permissions', enable each of the
   following permissions::

    * Create Instant Invite
    * Change Nickname
    * Create Expressions
    * Read Messages/View Channels
    * Create Events
    * Send Messages
    * Create Public Threads
    * Send Messages In Threads
    * Embed Links
    * Attach Files
    * Read Message History
    * Use External Emojis
    * Use External Stickers
    * Add Reactions
    * Use Slash Commands
    * Connect
    * Speak
    * Video
    * Use Voice Activity
    * Request To Speak
    * Use Embedded Activities
    * Use Soundboard
    * Use External Sounds

#. Copy the generated URL and open it in your
   web browser to add your bot to a server.


Running your bot
================

To run your version of the accord bot, make the
following changes to the df files:

* Open the 'default.env' file in located in::

    ~/dev/df/a3_src/h10_resource/key

* Paste your token to the following line and
  save the file::

    TOKEN_DISCORD_BOT_ACCORD='<YOUR_BOT_TOKEN>

* Go to the discord server where your bot has
  been added and check that it has been added.
* Once it has been added, make sure that the
  bot has the correct channels id's in::

    ~/df/a3_src/h60_system/accord/accord.stableflow.cfg.yaml

  This can be found under the
  ``# Discord bot integration.`` section where
  channel id's are listen next to the channel
  names. You can check channel names by right
  clicking on a channel in the discord and
  clicking ``Copy link`` The channel id it the
  last string of numbers that come after the
  last '/'.
* To start the bot change directory to::
    ~/dev/df
  and run::
    ./da demo start dm006 start
* If the bot works you should see log messages
  in the terminal after sending messages in the
  server.