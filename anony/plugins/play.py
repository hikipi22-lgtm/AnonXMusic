# Copyright (c) 2025 AnonymousX1025
from pathlib import Path
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from anony import anon, app, config, db, lang, queue, tg, yt
from anony.helpers import utils
from anony.helpers._play import checkUB

@app.on_message(
    filters.command(["play", "vplay"])
    & filters.group
    & ~app.bl_users
)
@lang.language()
@checkUB
async def play_hndlr(_, m: types.Message, video: bool = False):
    # 🔍 Original Search Text
    sent = await m.reply_text("🔍 **sᴇᴀʀᴄʜɪɴɢ...**")
    
    if len(m.command) < 2:
        return await sent.edit_text("❌ **ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ!**")

    query = " ".join(m.command[1:])
    file = await yt.search(query, sent.id, video=video)
    
    if not file:
        return await sent.edit_text("❌ **sᴏɴɢ ɴᴏᴛ ꜰᴏᴜɴᴅ!**")

    file.user = m.from_user.mention
    position = queue.add(m.chat.id, file)

    if position != 0 or await db.get_call(m.chat.id):
        # 📝 Queue UI with Buttons
        return await sent.edit_text(
            f"📝 **ǫᴜᴇᴜᴇᴅ ᴀᴛ #{position}**\n\n🎵 **ᴛɪᴛʟᴇ:** `{file.title}`\n⏱️ **ᴅᴜʀᴀᴛɪᴏɴ:** `{file.duration}`",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🗑 Cʟᴏsᴇ", callback_data="close")
            ]])
        )

    if not file.file_path:
        # 📥 Original Download Text
        await sent.edit_text("📥 **ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ...**")
        file.file_path = await yt.download(file.id, video=video)

    if not file.file_path:
        return await sent.edit_text("❌ **ʏᴏᴜᴛᴜʙᴇ ʙʟᴏᴄᴋ!** ᴜᴘᴅᴀᴛᴇ ᴄᴏᴏᴋɪᴇs.")

    await anon.play_media(chat_id=m.chat.id, message=sent, media=file)
