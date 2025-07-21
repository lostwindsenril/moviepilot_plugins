import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, List, Dict, Tuple, Optional

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app import schemas
from app.chain.storage import StorageChain
from app.core.config import settings
from app.core.event import eventmanager
from app.db.downloadhistory_oper import DownloadHistoryOper
from app.db.transferhistory_oper import TransferHistoryOper
from app.log import logger
from app.plugins import _PluginBase
from app.schemas import NotificationType, DownloadHistory
from app.schemas.types import EventType


class MyTestPlugin(_PluginBase):
    # 插件名称
    plugin_name = "测试插件"
    # 插件描述
    plugin_desc = "定时清理用户下载的种子、源文件、媒体库文件。"
    # 插件图标
    plugin_icon = "clean.png"
    # 插件版本
    plugin_version = "2.2"
    # 插件作者
    plugin_author = "thsrite"
    # 作者主页
    author_url = "https://github.com/thsrite"
    # 插件配置项ID前缀
    plugin_config_prefix = "mytestplugin_"
    # 加载顺序
    plugin_order = 23
    # 可使用的用户级别
    auth_level = 2

    # 私有属性
    _enabled = False
    # 任务执行间隔
    _cron = None
    _type = None
    _onlyonce = False
    _notify = False
    _cleantype = None
    _cleandate = None
    _cleanuser = None

    # 定时器
    _scheduler: Optional[BackgroundScheduler] = None

    def init_plugin(self, config: dict = None):
        pass