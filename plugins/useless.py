# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import psutil 
import time 

from pyrogram.types import Message
from pyrogram import Client, filters, StopPropagation
from config import OWNER_ID, BOT_STATS_TEXT, USER_REPLY_TEXT, USER_ROAST, ADMINS

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

from datetime import datetime
from helper_func import get_readable_time
from database.database import full_userbase, count_users, is_admin

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

ADMIN_COMMANDS = [
    "addadmin", "deladmin", "admins",
    "reqtime", "reqmode", "approveoff", "approveon",
    "addchat", "addch", "delchat", "delch", "ch_links", "reqlink", "links", "bulklink", "genlink", "channels",
    "status", "cancel", "broadcast",
    "add_fsub", "del_fsub", "fsub",
    "stats", "ban"
]

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

@Client.on_message(filters.command(ADMIN_COMMANDS), group=-2)
async def admin_command_interceptor(bot: Client, message: Message):
    if not message.from_user:
        return
    
    user_id = message.from_user.id
    
    # Check if user is owner or admin
    is_authorized = (user_id == OWNER_ID) or (user_id in ADMINS) or (await is_admin(user_id))
    
    if not is_authorized:
        command = message.command[0].lower() if message.command else ""
        if command in ["ban", "broadcast"]:
            if USER_ROAST:
                await message.reply_text(USER_ROAST)
        else:
            if USER_REPLY_TEXT:
                await message.reply_text(USER_REPLY_TEXT)
        
        # Stop further handling of this message
        raise StopPropagation

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# --- 1. NORMAL USER KE LIYE AUTO-REPLY ---
# Isme humne commands ko exclude kar diya hai (~filters.command)
@Client.on_message(filters.private & filters.incoming & filters.text & ~filters.regex(r"^/"))
async def useless_reply(bot: Client, message: Message):
    user_id = message.from_user.id
    if user_id != OWNER_ID: # Sirf unko reply jaye jo owner nahi hain
        if USER_REPLY_TEXT:
            await message.reply_text(USER_REPLY_TEXT)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# --- 2. STATS COMMAND (WITH SECURITY) ---
@Client.on_message(filters.command("stats") & filters.private)
async def stats(bot: Client, message: Message):
    user_id = message.from_user.id

    if user_id != OWNER_ID:
        if USER_REPLY_TEXT:
            await message.reply_text(USER_REPLY_TEXT)
        return

    start = time.time()
    wait = await message.reply_text("<code>📊 Extracting Statistics...</code>")

    # Ping
    ping = (time.time() - start) * 1000

    # Uptime
    now = datetime.now()
    delta = now - bot.uptime
    uptime = get_readable_time(int(delta.total_seconds()))

    # Users
    try:
        users = await count_users()
    except:
        users = 0

    # RAM
    ram = psutil.virtual_memory()
    ram_percent = ram.percent

    # CPU
    cpu_percent = psutil.cpu_percent(interval=1)

    # Disk
    disk = psutil.disk_usage("/")
    disk_percent = disk.percent

    used = disk.used / (1024 ** 3)
    free = disk.free / (1024 ** 3)
    total = disk.total / (1024 ** 3)

    def progress(percent):
        filled = int(percent // 10)
        if filled >= 10:
            return "■" * 10
        return "■" * filled + "▤" + "□" * (9 - filled)

    text = f"""
<b>⌬ 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 :</b>

┎ <b>Bᴏᴛ Uᴘᴛɪᴍᴇ :</b> <code>{uptime}</code>
┃ <b>Cᴜʀʀᴇɴᴛ Pɪɴɢ :</b> <code>{ping:.3f} ms</code>
┖ <b>Tᴏᴛᴀʟ Uꜱᴇʀꜱ :</b> <code>{users}</code>

┎ <b>RAM ( MEMORY ) :</b>
┖ <code>[{progress(ram_percent)}] {ram_percent:.1f}%</code>

┎ <b>CPU ( USAGE ) :</b>
┖ <code>[{progress(cpu_percent)}] {cpu_percent:.1f}%</code>

┎ <b>DISK :</b>
┃ <code>[{progress(disk_percent)}] {disk_percent:.1f}%</code>
┃ <b>Usᴇᴅ :</b> <code>{used:.2f} GB</code>
┃ <b>Fʀᴇᴇ :</b> <code>{free:.2f} GB</code>
┖ <b>Tᴏᴛᴀʟ :</b> <code>{total:.2f} GB</code>
"""

    await wait.edit_text(text)
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #