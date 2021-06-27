from nonebot import require

import requests
import json
import os

scheduler = require('nonebot_plugin_apscheduler').scheduler

@scheduler.scheduled_job('cron', second="*/10", id='sub_check')
async def run_every_10_seconds():
    file_path = "/root/qqBot/NothAmor-Bot/nothamor_bot/plugins/stream_sub/sub.json"
    cq_api = "http://kod.nothamor.cn:5700/send_group_msg?group_id={}&message={}"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
        "Cookie": "_uuid=A84EE9DB-6F1E-23A9-6143-C12F0452F1AA09526infoc; buvid3=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(u)Yl|YummR0J'uYuY|lYml|; fingerprint=7bfed0535c2f297ab55b045f06a84e24; buvid_fp=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; buvid_fp_plain=C2001EF8-B63F-4BFE-A82F-B874767350BE138387infoc; SESSDATA=43a18e0d%2C1634741154%2C55936%2A41; bili_jct=2de33df16746e3f118d41a384666c344; DedeUserID=36409264; DedeUserID__ckMd5=89cb10047d92a5b5; sid=anjfrwb7; LIVE_BUVID=AUTO6616204776752283; bp_video_offset_36409264=537582347573076463; CURRENT_QUALITY=80; bsource=search_bing; _dfcaptcha=4fed6d52ff72669b763551d36f761d20; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624547492,1624547545,1624547563,1624796501; Hm_lpvt_8a6e55dbd2870f0f5bc9194cddf32a02=1624796501; PVID=14",
        "Content-Type": "application/json"
    }

    with open(file_path, "r") as file:
        file_data = json.load(file)

        for room in file_data["sub"]:
            room_id = room["sub_user_id"]
            at_ = "[CQ:at,qq={}]".format(room["sub_user"])

            room_api = json.loads(requests.get("https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={}".format(str(room_id)), headers=header).text)

            room_status = room_api["data"]["liveStatus"]
            if room_status == 1 and room["live_status"] == False:
                requests.get(cq_api.format(room["sub_group"], "直播间 '{}' 开播啦! 快来收看吧~ {} 此直播间由 {} 订阅!".format(room_api["data"]["title"], room_api["data"]["link"].split("?")[0], at_)))

                update_live_status = {
                    "live_status": True
                }
                room.update(update_live_status)
                open(file_path, "wb+").write(json.dumps(file_data).encode())
            elif room_status == 0 and room["live_status"] == True:
                update_live_status = {
                    "live_status": False
                }
                room.update(update_live_status)
                open(file_path, "wb+").write(json.dumps(file_data).encode())

scheduler.add_job(run_every_10_seconds, "crob", second="*/10")