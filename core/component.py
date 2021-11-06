import re
from typing import Union

from apscheduler.triggers.combining import AndTrigger, OrTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from core.elements import Command, RegexCommand, Option, Schedule, StartUp
from core.loader import ModulesManager
from core.elements.module.meta import *


class Bind:
    class Command:
        def __init__(self, bind_prefix):
            self.bind_prefix = bind_prefix

        def handle(self,
                   help_doc: str = None,
                   required_admin: bool = False,
                   required_superuser: bool = False):
            def decorator(function):
                ModulesManager.bind_to_module(self.bind_prefix, CommandMeta(function=function,
                                                                            help_doc=help_doc,
                                                                            required_admin=required_admin,
                                                                            required_superuser=required_superuser))

            return decorator

    class Regex:
        def __init__(self, bind_prefix):
            self.bind_prefix = bind_prefix

        def handle(self, pattern: str, mode: str = "M", flags: re.RegexFlag = 0, show_typing: bool = True):
            def decorator(function):
                ModulesManager.bind_to_module(self.bind_prefix, RegexMeta(function=function,
                                                                          pattern=pattern,
                                                                          mode=mode,
                                                                          flags=flags,
                                                                          show_typing=show_typing))

            return decorator

    class Schedule:
        def __init__(self, bind_prefix):
            self.bind_prefix = bind_prefix

        def handle(self):
            def decorator(function):
                ModulesManager.bind_to_module(self.bind_prefix, ScheduleMeta(function=function))

            return decorator


def on_command(
        bind_prefix: str,
        alias: Union[str, list, tuple, dict] = None,
        desc: str = None,
        recommend_modules: Union[str, list, tuple] = None,
        developers: Union[str, list, tuple] = None,
        required_admin: bool = False,
        base: bool = False,
        required_superuser: bool = False
):
    """

    :param bind_prefix: 绑定的命令前缀。
    :param alias: 此命令的别名。
    同时被用作命令解析，当此项不为空时将会尝试解析其中的语法并储存结果在 MessageSession.parsed_msg 中。
    :param desc: 此命令的简介。
    :param recommend_modules: 推荐打开的其他模块。
    :param developers: 模块作者。
    :param required_admin: 此命令是否需要群聊管理员权限。
    :param base: 将此命令设为基础命令。设为基础命令后此命令将被强制开启。
    :param required_superuser: 将此命令设为机器人的超级管理员才可执行。
    :return: 此类型的模块。
    """
    module = Command(alias=alias,
                     bind_prefix=bind_prefix,
                     desc=desc,
                     recommend_modules=recommend_modules,
                     developers=developers,
                     base=base,
                     required_admin=required_admin,
                     required_superuser=required_superuser)
    ModulesManager.add_module(module)
    return Bind.Command(bind_prefix)


def on_regex(
        bind_prefix: str,
        recommend_modules: Union[str, list, tuple] = None,
        alias: Union[str, list, tuple, dict] = None,
        desc: str = None,
        developers: Union[str, list, tuple] = None,
        required_admin: bool = False,
        base: bool = False,
        required_superuser: bool = False):
    """

    :param bind_prefix: 绑定的命令前缀。
    模式所获取到的内容将会储存在 MessageSession.matched_msg 中。
    :param alias: 此命令的别名。
    :param desc: 此命令的简介。
    :param recommend_modules: 推荐打开的其他模块。
    :param developers: 模块作者。
    :param required_admin: 此命令是否需要群聊管理员权限。
    :param base: 将此命令设为基础命令。设为基础命令后此命令将被强制开启。
    :param required_superuser: 将此命令设为机器人的超级管理员才可执行。
    :return: 此类型的模块。
    """

    module = RegexCommand(bind_prefix=bind_prefix,
                          recommend_modules=recommend_modules,
                          alias=alias,
                          desc=desc,
                          developers=developers,
                          required_admin=required_admin,
                          base=base,
                          required_superuser=required_superuser,
                          )
    ModulesManager.add_module(module)
    return Bind.Regex(bind_prefix)


def on_option(
        bind_prefix: str,
        desc: str = None,
        alias: Union[str, list, tuple, dict] = None,
        recommend_modules: Union[str, list, tuple] = None,
        developers: Union[str, list, tuple] = None,
        required_superuser: bool = False,
        required_admin: bool = False
):
    """

    :param bind_prefix: 绑定的命令前缀。
    :param alias: 此命令的别名。
    :param desc: 此命令的简介。
    :param recommend_modules: 推荐打开的其他模块。
    :param developers: 模块作者。
    :param required_admin: 此命令是否需要群聊管理员权限。
    :param required_superuser: 将此命令设为机器人的超级管理员才可执行。
    :return: 此类型的模块。
    """

    module = Option(bind_prefix=bind_prefix,
                    desc=desc,
                    alias=alias,
                    recommend_modules=recommend_modules,
                    developers=developers,
                    required_superuser=required_superuser,
                    required_admin=required_admin)
    ModulesManager.add_module(module)


def on_schedule(
        bind_prefix: str,
        trigger: Union[AndTrigger, OrTrigger, DateTrigger, CronTrigger, IntervalTrigger],
        desc: str = None,
        alias: Union[str, list, tuple, dict] = None,
        recommend_modules: Union[str, list, tuple] = None,
        developers: Union[str, list, tuple] = None,
        required_superuser: bool = False,
):
    """
    :param bind_prefix: 绑定的命令前缀。
    :param trigger: 此命令的触发器。
    :param alias: 此命令的别名。
    :param desc: 此命令的简介。
    :param recommend_modules: 推荐打开的其他模块。
    :param developers: 模块作者。
    :param required_superuser: 将此命令设为机器人的超级管理员才可执行。
    :return: 此类型的模块。
    """

    def decorator(function):
        module = Schedule(function=function,
                          trigger=trigger,
                          bind_prefix=bind_prefix,
                          desc=desc,
                          alias=alias,
                          recommend_modules=recommend_modules,
                          developers=developers,
                          required_superuser=required_superuser)
        ModulesManager.add_module(module)
        return module

    return decorator


def on_startup(
        bind_prefix: str,
        desc: str = None,
        alias: Union[str, list, tuple, dict] = None,
        recommend_modules: Union[str, list, tuple] = None,
        developers: Union[str, list, tuple] = None,
        required_superuser: bool = False,
):
    """

    :param bind_prefix: 绑定的命令前缀。
    :param alias: 此命令的别名。
    :param desc: 此命令的简介。
    :param recommend_modules: 推荐打开的其他模块。
    :param developers: 模块作者。
    :param required_superuser: 将此命令设为机器人的超级管理员才可执行。
    :return: 此类型的模块。
    """

    def decorator(function):
        module = StartUp(function=function,
                         bind_prefix=bind_prefix,
                         desc=desc,
                         alias=alias,
                         recommend_modules=recommend_modules,
                         developers=developers,
                         required_superuser=required_superuser)
        ModulesManager.add_module(module)
        return module

    return decorator