# This is code to clone the gdrive link using the gclone, all credit goes to the developer who has developed the rclone/glclone
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) gautamajay52
# (c) MaxxRider

import asyncio
import logging
import os
import re
import subprocess

import pyrogram.types as pyrogram
import requests
from tobrot import (
    DESTINATION_FOLDER,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    INDEX_LINK,
    LOGGER,
    RCLONE_CONFIG,
    TG_MAX_FILE_SIZE,
    UPLOAD_AS_DOC,
)
from re import search
from urllib.parse import parse_qs, urlparse

class CloneHelper:
    def __init__(self, mess):
        self.g_id = ""
        self.mess = mess
        self.name = ""
        self.out = b""
        self.err = b""
        self.lsg = ""
        self.filee = ""
        self.u_id = self.mess.from_user.id
        self.u_men = self.mess.from_user.mention
        self.dname = ""

    def config(self):
        if not os.path.exists("rclone.conf"):
            with open("rclone.conf", "w+", newline="\n", encoding="utf-8") as fole:
                fole.write(f"{RCLONE_CONFIG}")
        if os.path.exists("rclone.conf"):
            with open("rclone.conf", "r+") as file:
                con = file.read()
                self.dname = re.findall("\[(.*)\]", con)[0]

    def get_id(self):
        mes = self.mess
        reply_to = mes.reply_to_message
        LOGGER.info(txt)
        mystery = mes.text.split(" ", maxsplit=1)
        if mystery > 1:
            txt = mystery[1]
        else:
            txt = reply_to.text 
        mess = txt.split("|", maxsplit=1)
        if len(mess) == 2:
            self.g_id = self.getIdFromUrl(mess[0])
            LOGGER.info(self.g_id)
            self.name = mess[1]
            LOGGER.info(self.name)
        else:
            self.g_id = self.getIdFromUrl(mess[0])
            LOGGER.info(self.g_id)
            self.name = ""
        return self.g_id, self.name

    @staticmethod
    def getIdFromUrl(link: str):
        if "folders" in link or "file" in link:
            regex = r"https:\/\/drive\.google\.com\/(?:drive(.*?)\/folders\/|file(.*?)?\/d\/)([-\w]+)"
            res = search(regex,link)
            if res is None:
                LOGGER.info("G-Drive ID not found.")
            return res.group(3)
        parsed = urlparse(link)
        return parse_qs(parsed.query)['id'][0]

    async def link_gen_size(self):
        if self.name is not None:
            _drive = ""
            if self.name == self.filee:
                _flag = "--files-only"
                _up = "File"
                _ui = ""
            else:
                _flag = "--dirs-only"
                _up = "Folder"
                _drive = "folderba"
                _ui = "/"
            g_name = re.escape(self.name)
            LOGGER.info(g_name)
            destination = f"{DESTINATION_FOLDER}"

            with open("filter1.txt", "w+", encoding="utf-8") as filter1:
                print(f"+ {g_name}{_ui}\n- *", file=filter1)

            g_a_u = [
                "rclone",
                "lsf",
                "--config=./rclone.conf",
                "-F",
                "i",
                "--filter-from=./filter1.txt",
                f"{_flag}",
                f"{self.dname}:{destination}",
            ]
            LOGGER.info(g_a_u)
            gau_tam = await asyncio.create_subprocess_exec(
                *g_a_u, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            gau, tam = await gau_tam.communicate()
            LOGGER.info(gau)
            gautam = gau.decode("utf-8")
            LOGGER.info(gautam)
            LOGGER.info(tam.decode("utf-8"))

            if _drive == "folderba":
                gautii = f"https://drive.google.com/folderview?id={gautam}"
            else:
                gautii = f"https://drive.google.com/file/d/{gautam}/view?usp=drivesdk"

            LOGGER.info(gautii)
            gau_link = re.search("(?P<url>https?://[^\s]+)", gautii).group("url")
            LOGGER.info(gau_link)
            button = []
            button.append(
                [
                    pyrogram.InlineKeyboardButton(
                        text="☁️ GDrive Link ☁️", url=f"{gau_link}"
                    )
                ]
            )
            if INDEX_LINK:
                _idno = 1
                for indexes in INDEX_LINK:
                    if _flag == "--files-only":
                        indexurl = f"{indexes}/{self.name}"
                    else:
                        indexurl = f"{indexes}/{self.name}/"
                    tam_link = requests.utils.requote_uri(indexurl)
                    LOGGER.info(tam_link)
                    button.append(
                        [
                            pyrogram.InlineKeyboardButton(
                                text=f"⚡️ Index Link #{_idno}⚡️", url=f"{tam_link}"
                            )
                        ]
                    )
                    _idno = _idno + 1
            button_markup = pyrogram.InlineKeyboardMarkup(button)
            msg = await self.lsg.edit_text(
                f"🐈: {_up} Cloned successfully in your Cloud <a href='tg://user?id={self.u_id}'>😊</a>\
                \n📀 Info: Calculating...",
                reply_markup=button_markup,
                parse_mode="html",
            )
            g_cmd = [
                "rclone",
                "size",
                "--config=rclone.conf",
                f"{self.dname}:{destination}/{self.name}",
            ]
            LOGGER.info(g_cmd)
            gaut_am = await asyncio.create_subprocess_exec(
                *g_cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            gaut, am = await gaut_am.communicate()
            g_autam = gaut.decode("utf-8")
            LOGGER.info(g_autam)
            LOGGER.info(am.decode("utf-8"))
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await msg.edit_text(
                f"{_up} Cloned successfully in your Cloud <a href='tg://user?id={self.u_id}'>😊</a>\
                \n☁️ Info:\n{g_autam}\n\n**Req By**: {self.u_men}",
                reply_markup=button_markup,
                parse_mode="html",
            )

    async def gcl(self):
        self.lsg = await self.mess.reply_text(f"Cloning...you should wait 🤒")
        destination = f"{DESTINATION_FOLDER}"
        idd = "{" f"{self.g_id}" "}"
        cmd = [
            "/app/gautam/gclone",
            "copy",
            "--config=rclone.conf",
            f"{self.dname}:{idd}",
            f"{self.dname}:{destination}/{self.name}",
            "-v",
            "--drive-server-side-across-configs",
            "--transfers=16",
            "--checkers=20",
        ]
        LOGGER.info(cmd)
        pro = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        p, e = await pro.communicate()
        self.out = p
        LOGGER.info(self.out)
        err = e.decode()
        LOGGER.info(err)
        LOGGER.info(self.out.decode())

        if self.name == "":
            reg_f = "INFO(.*)(:)(.*)(:) (Copied)"
            file_n = re.findall(reg_f, err)
            LOGGER.info(file_n[0][2].strip())
            self.name = file_n[0][2].strip()
            self.filee = self.name
