# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.discord.bot

"""


import inspect
import time

import psutil
import pytest


# =============================================================================
class SpecifyFlNetDiscordBot:
    """
    Spec for the fl.net.discord.bot module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_net_discord_bot(self):
        """
        fl.net.discord.bot can be imported.

        """
        import fl.net.discord.bot


# =============================================================================
class SpecifyFlNetDiscordBotCoro:
    """
    Spec for the fl.net.discord.bot.coro coroutine function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_run(self):
        """
        fl.net.discord.bot.coro can be initialized as a generator.

        """

        import fl.net.discord.bot
        import key

        # bot.coro is a generator function, and
        # when we run it it spawns a subprocess.
        #
        str_token         = key.load('TOKEN_DISCORD_DEFAULT')
        proc_child_before = psutil.Process().children()
        cfg_bot           = dict(str_token  = str_token,
                                 secs_sleep = 0.1,
                                 id_system  = 'test',
                                 id_node    = 'discord-bot')
        bot               = fl.net.discord.bot.coro(cfg_bot = cfg_bot)
        assert inspect.isgenerator(bot)
        for _ in range(40):
            time.sleep(0.05)
            proc_child_after = psutil.Process().children()
            if proc_child_after != proc_child_before:
                break
        assert proc_child_after != proc_child_before

        # Sending nothing gets nothing back.
        #
        list_to_bot = []

        (list_from_bot) = bot.send(list_to_bot)

        assert list_from_bot == []
