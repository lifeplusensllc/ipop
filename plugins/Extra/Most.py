import re
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from database.config_db import mdb

# most search commands
@Client.on_message(filters.command('most'))
async def most(client, message):

    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    
    try:
        limit = int(message.command[1])
    except (IndexError, ValueError):
        limit = 20

    top_messages = await mdb.get_top_messages(limit)

    # Use a set to ensure unique messages (case sensitive).
    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        # Check if message already exists in the set (case sensitive)
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            if len(msg) > 35:
                truncated_messages.append(msg[:35 - 3])
            else:
                truncated_messages.append(msg)

    keyboard = []
    for i in range(0, len(truncated_messages), 2):
        row = truncated_messages[i:i+2]
        keyboard.append(row)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, placeholder="Most searches of the day")
    m=await message.reply_text("⏳️ ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡᴇ ᴀʀᴇ ꜰᴇᴛᴄʜɪɴɢ ᴛᴏᴘ ᴛʀᴇɴᴅɪɴɢ ꜱᴇᴀʀᴄʜ..")
    await m.edit_text("⏳️ ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴡᴇ ᴀʀᴇ ꜰᴇᴛᴄʜɪɴɢ ᴛᴏᴘ ᴛʀᴇɴᴅɪɴɢ ꜱᴇᴀʀᴄʜ...")
    await m.delete()
    await message.reply_text(f"<b>✨️ ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴛʀᴇɴᴅɪɴɢ ꜱᴇᴀʀᴄʜᴇꜱ ᴏꜰ ᴛʜᴇ ᴅᴀʏ -</b>", reply_markup=reply_markup)

    
@Client.on_message(filters.command('mostlist'))
async def trendlist(client, message):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))

    # Set the limit to the default if no argument is provided
    limit = 31

    # Check if an argument is provided and if it's a valid number
    if len(message.command) > 1:
        try:
            limit = int(message.command[1])
        except ValueError:
            await message.reply_text("Invalid number format.\nPlease provide a valid number after the /trendlist command.")
            return  # Exit the function if the argument is not a valid integer

    try:
        top_messages = await mdb.get_top_messages(limit)
    except Exception as e:
        await message.reply_text(f"Error retrieving messages: {str(e)}")
        return  # Exit the function if there is an error retrieving messages

    if not top_messages:
        await message.reply_text("No most messages found.")
        return  # Exit the function if no messages are found

    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            # Add an ellipsis to indicate the message has been truncated
            truncated_messages.append(msg[:32] + '...' if len(msg) > 35 else msg)

    if not truncated_messages:
        await message.reply_text("No valid most messages found.")
        return  # Exit the function if no valid messages are found

    # Create a formatted text list
    formatted_list = "\n".join([f"{i+1}. <b>{msg}</b>" for i, msg in enumerate(truncated_messages)])

    # Append the additional message at the end
    additional_message = "ᴀʟʟ ᴛʜᴇ ʀᴇsᴜʟᴛs ᴀʙᴏᴠᴇ ᴄᴏᴍᴇ ғʀᴏᴍ ᴡʜᴀᴛ ᴜsᴇʀs ʜᴀᴠᴇ sᴇᴀʀᴄʜᴇᴅ ғᴏʀ 🔎"
    formatted_list += f"\n\n{additional_message}"

    reply_text = f"<b><u>📍 ᴛᴏᴘ {len(truncated_messages)} 📈 ᴍᴏsᴛ sᴇᴀʀᴄʜᴇs ʟɪsᴛ:</u></b>\n\n{formatted_list}"
    
    await message.reply_text(reply_text)
