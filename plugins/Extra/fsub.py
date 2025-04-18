from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL
from utils import is_check_admin
import logging  
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("fsub"))
async def force_subscribe(client, message):
    m = await message.reply_text("Wait im checking...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs 💢**")
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("**ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ! 💼**")
    try: 
        toFsub = message.command[1]
    except IndexError:
        return await m.edit("**ᴜsᴀɢᴇ - /fsub ᴄʜᴀᴛ_ɪᴅ**")
    if not toFsub.startswith("-100"):
        toFsub = '-100'+toFsub
    if not toFsub[1:].isdigit() or len(toFsub) != 14:
        return await m.edit("**ᴄʜᴀᴛ_ɪᴅ ɪsɴ'ᴛ ᴠᴀʟɪᴅ! 🚫**")
    toFsub = int(toFsub)
    if toFsub == message.chat.id:
        return await m.edit("**ᴘʟᴇᴀsᴇ ᴜsᴇ ᴀ ᴅɪғғᴇʀᴇɴᴛ ᴄʜᴀᴛ ɪᴅ! ✴️**")
    if not await is_check_admin(client, toFsub, client.me.id):
        return await m.edit("<b>ɪ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ɢɪᴠᴇɴ ᴄʜᴀᴛ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ!\n<u>ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ᴛᴀʀɢᴇᴛ ᴄʜᴀᴛ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ.</u></b>")
    try:
        await db.setFsub(grpID=message.chat.id, fsubID=toFsub)
        return await m.edit(f"**✅ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴛᴏ {toFsub} {message.chat.title}**")
    except Exception as e:
        logger.exception(e)
        return await m.edit(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ ᴏʀ ʀᴇᴘᴏʀᴛ ɪɴ @I_M_STARBOY **")

@Client.on_message(filters.command("del_fsub"))
async def del_force_subscribe(client, message):
    m = await message.reply_text("**⏳ ᴡᴀɪᴛ ɪᴍ ᴄʜᴇᴄᴋɪɴɢ...**")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs 💢**")
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("")
    ifDeleted =await db.delFsub(message.chat.id)
    if ifDeleted:
        return await m.edit(f"**🚫 sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ғᴏʀ - {message.chat.title}\nᴛᴏ ᴀᴅᴅ ᴀɢᴀɪɴ ᴜsᴇ <code>/fsub YOUR_FSUB_CHAT_ID</code>**")
    else:
        return await m.edit(f"**ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ❌ {message.chat.title}**")

@Client.on_message(filters.command("show_fsub"))
async def show_fsub(client, message):
    m = await message.reply_text("⏳ ᴡᴀɪᴛ ɪᴍ ᴄʜᴇᴄᴋɪɴɢ...")
    if not message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs 💢**")
    # check if commad is given by admin or not
    if not await is_check_admin(client, message.chat.id, message.from_user.id):
        return await m.edit("**ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ! 💼**")
    fsub = await db.getFsub(message.chat.id)
    if fsub:
        #now gen a invite link
        invite_link = await client.export_chat_invite_link(fsub)
        await m.edit(f"» ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs sᴇᴛ ᴛᴏ {fsub}\n<a href={invite_link}» ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ </a>" ,disable_web_page_preview=True)
    else:
        await m.edit(f"**ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ɪs ɴᴏᴛ sᴇᴛ ɪɴ {message.chat.title} ❌ **")
