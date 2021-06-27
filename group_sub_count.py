from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.cqhttp import Bot, Message
from nonebot.rule import to_me
from nonebot.typing import T_State
import requests
import json

stream_sub_list = on_command('stream_sub_list', aliases=set(['群直播间订阅列表']))


@stream_sub_list.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    file_path = "/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/stream_sub/sub.json"
    file_data = json.load(open(file_path, "r"))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        "Cookie": "_uuid=A84EE9DB-6F1E-23A9-6143-C12F0452F1AA09526infoc; buvid3=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u)Yl|YummR0J'uYuY|lYml|; fingerprint=7bfed0535c2f297ab55b045f06a84e24; buvid_fp=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; buvid_fp_plain=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; SESSDATA=43a18e0d%2C1634741154%2C55936%2A41; bili_jct=2de33df16746e3f118d41a384666c344; DedeUserID=36409264; DedeUserID__ckMd5=89cb10047d92a5b5; sid=anjfrwb7; LIVE_BUVID=AUTO6616204776752283; bp_video_offset_36409264=537582347573076463; CURRENT_QUALITY=80; bsource=search_bing; _dfcaptcha=4fed6d52ff72669b763551d36f761d20; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624547492,1624547545,1624547563,1624796501; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624796501; PVID=14",
        "Content-Type": "application/json"
    }

    count = 0
    content = ""
    for i in file_data["sub"]:
        if i["sub_group"] == str(event.group_id):
            count += 1
            room_api = json.loads(requests.get("https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={}".format(str(i["sub_user_id"])), headers=header).text)
            content += """{}. {}
            """.format(count, room_api["data"]["title"])

    await stream_sub_list.send(Message("""本群中共订阅了{}个直播间
    {}""".format(count, content)))