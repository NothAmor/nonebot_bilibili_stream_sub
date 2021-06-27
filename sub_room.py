from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import Message

import os
import json

stream_sub = on_command("直播间订阅")

@stream_sub.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).lstrip()
    if args:
        state["sentence"] = args

@stream_sub.got("sentence", prompt="订阅哪个用户的直播间? 请输入用户ID! (只支持哔哩哔哩订阅)")
async def handle_city(bot: Bot, event: Event, state: T_State):
    sentence = state["sentence"]
    file = "/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/stream_sub/sub.json"

    if "http" in sentence or "https" in sentence:
        split_last = sentence.split("/")
        if split_last[-1] == "":
            sentence = split_last[-2]
        else:
            sentence = split_last[-1]

    sub_data = {
        "sub_user_id": sentence,
        "sub_user": str(event.get_user_id()),
        "sub_group": str(event.group_id),
        "live_status": False
    }

    if open(file, "r").read() == "":
        file_data = {
            "sub": [{
                "sub_user_id": sentence,
                "sub_user": str(event.get_user_id()),
                "sub_group": str(event.group_id),
                "live_status": False
            }]
        }
        open(file, "wb+").write(json.dumps(file_data).encode())
    else:
        file_data = json.load(open(file, "r"))

        flag = False
        for data in file_data["sub"]:
            if data["sub_user_id"] == sentence and data["sub_group"] == str(event.group_id):
                await stream_sub.send(Message("此群聊中已经订阅了哔哩哔哩用户ID为 {} 的直播间了!".format(sentence)))
                flag = True

        if flag == False:
            file_data["sub"].append(sub_data)
            open(file, "w").write(json.dumps(file_data))
            await stream_sub.send(Message("订阅成功!"))