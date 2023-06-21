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
        str_token         = key.load('TOKEN_DISCORD_BOT_ACCORD')
        proc_child_before = psutil.Process().children()
        bot               = fl.net.discord.bot.coro({'str_token':  str_token,
                                                     'secs_sleep': 0.1 })
        assert inspect.isgenerator(bot)
        for _ in range(40):
            time.sleep(0.05)
            proc_child_after = psutil.Process().children()
            if proc_child_after != proc_child_before:
                break
        assert proc_child_after != proc_child_before

        # Sending nothing gets nothing back.
        #
        list_msg_to_bot = []
        list_cmd_to_bot = []

        (list_msg_from_bot,
         list_cmd_from_bot,
         list_log_from_bot) = bot.send((list_msg_to_bot,
                                        list_cmd_to_bot))

        assert list_msg_from_bot == []
        assert list_cmd_from_bot == []
        # assert list_log_from_bot == []
