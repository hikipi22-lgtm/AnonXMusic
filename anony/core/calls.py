from pyrogram.types import InputMediaPhoto
from pytgcalls import PyTgCalls, types
from pytgcalls.pytgcalls_session import PyTgCallsSession
from anony import app, db, logger, queue, userbot, yt
from anony.helpers import buttons

class TgCall(PyTgCalls):
    def __init__(self):
        self.clients = []

    async def play_media(self, chat_id: int, media, message=None):
        client = await db.get_assistant(chat_id)
        stream = types.MediaStream(
            media_path=media.file_path,
            audio_parameters=types.AudioQuality.HIGH,
            video_parameters=types.VideoQuality.HD_720p,
        )
        try:
            await client.play(chat_id, stream)
            if message:
                # ✨ ASLI ORIGINAL UI (As per your Screenshot)
                text = (
                    f"**| Started streaming**\n\n"
                    f"**Title:** [{media.title}]({media.url})\n\n"
                    f"**Duration:** {media.duration} min\n"
                    f"**Requested by:** {media.user}"
                )
                try:
                    # Using actual YouTube thumbnail
                    await message.edit_media(
                        media=InputMediaPhoto(media=media.thumb, caption=text)
                    )
                except:
                    # Fallback to text if media fails
                    await message.edit_text(text)
        except Exception as e:
            logger.error(f"Play Error: {e}")

    async def boot(self) -> None:
        PyTgCallsSession.notice_displayed = True
        for ub in userbot.clients:
            client = PyTgCalls(ub)
            await client.start()
            self.clients.append(client)
        logger.info("Bot Started with Original UI!")
