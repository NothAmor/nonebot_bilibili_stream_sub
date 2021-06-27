from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message

import os
import json

stream_sub_delete = on_command("群直播间订阅删除")

@stream_sub_delete.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).lstrip()
    if args:
        state["sentence"] = args

@stream_sub_delete.got("sentence", prompt="请输入想要删除的直播ID")
async def handle_city(bot: Bot, event: Event, state: T_State):
    sentence = state["sentence"]
    file = "/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/stream_sub/sub.json"
    file_data = json.load(open(file, "r"))

    count = 0
    for i in file_data["sub"]:
        if i["sub_user_id"] == sentence:
            del file_data["sub"][count]
        count += 1
    
    with open(file, "wb+") as obj:
        obj.write(json.dumps(file_data))

    await stream_sub_delete.send(Message("删除成功!"))