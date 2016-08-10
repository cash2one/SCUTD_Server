# -*- coding: utf-8 -*-

__all__ = ['WechatBasic', 'WechatExt']

try:
    from wechat_sdk_.basic import WechatBasic
    from wechat_sdk_.ext import WechatExt
except ImportError:
    pass