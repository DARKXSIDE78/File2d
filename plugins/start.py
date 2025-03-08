#(©)CodeXBotz

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery  # Add CallbackQuery here

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, START_PIC, AUTO_DELETE_TIME, AUTO_DELETE_MSG, JOIN_REQUEST_ENABLE,FORCE_SUB_CHANNEL,FORCE_SUB_CHANNEL2,FORCE_SUB_CHANNEL3,FORCE_SUB_CHANNEL4
from helper_func import subscribed,decode, get_messages, delete_file
from database.database import add_user, del_user, full_userbase, present_user


@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        track_msgs = []

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(previouscaption="" if not msg.caption else msg.caption.html, filename=msg.document.file_name)
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            if AUTO_DELETE_TIME and AUTO_DELETE_TIME > 0:
                try:
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        print("Failed to copy message, skipping.")
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    copied_msg_for_deletion = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    if copied_msg_for_deletion:
                        track_msgs.append(copied_msg_for_deletion)
                    else:
                        print("Failed to copy message after retry, skipping.")
                except Exception as e:
                    print(f"Error copying message: {e}")
                    pass
            else:
                try:
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                    await asyncio.sleep(0.5)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                    await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                except:
                    pass

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            # Schedule the file deletion task after all messages have been copied
            asyncio.create_task(delete_file(track_msgs, client, delete_data))
        else:
            print("No messages to track for deletion.")

        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡️ ᴍᴀɪɴ ʜᴜʙ", url="t.me/Anime_Movies_Hindi_Dub_India"),
                    InlineKeyboardButton("🍁 ᴏᴡɴᴇʀ", url="t.me/Shikamaru_Naru")
                ],
                [
                    InlineKeyboardButton("🛈 ᴀʙᴏᴜᴛ", callback_data = "about"),
                    InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data = "close")
                ]
            ]
        )
        if START_PIC:  # Check if START_PIC has a value
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:  # If START_PIC is empty, send only the text
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        return

@Bot.on_callback_query(filters.regex('about'))
async def about_callback(client: Client, callback_query: CallbackQuery):
    # Send some info about the bot
    await callback_query.answer()
    await callback_query.message.edit_text(
    "<b>○ Cʀᴇᴀᴛᴏʀ: <a href='https://t.me/Shikamaru_Naru'>Shikamaru</a></b>\n"
    "<b>○ Lᴀɴɢᴜᴀɢᴇ: <a href='https://www.python.org/downloads/'>Pʏᴛʜᴏɴ</a></b\n"
    "<b>○ Lɪʙʀᴀʀʏ: <a href='https://github.com/pyrogram/pyrogram'>Pʏʀᴏɢʀᴀᴍ</a></b\n"
    "<b>○ Mᴀɪɴ Cʜᴀɴɴᴇʟ: <a href='https://t.me/Anime_Movies_Hindi_Dub_India'>Aɴɪᴍᴇ</a></b\n",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data= "close")
                ]
            ]
        )
    )

# Callback handler for the "✘ ᴄʟᴏsᴇ" button
@Bot.on_callback_query(filters.regex('close'))
async def close_callback(client: Client, callback_query: CallbackQuery):
    # Close the current message
    await callback_query.answer()
    await callback_query.message.delete()

#=====================================================================================##

WAIT_MSG = """"<b>Pʀᴏᴄᴇssɪɴɢ...</b>"""

REPLY_ERROR = """<code>Use this command as a reply to any telegram message without any spaces.</code>"""

#=====================================================================================##

@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    # List of all the force subscription channels
    force_sub_channels = [
        {"id": FORCE_SUB_CHANNEL, "name": "Jᴏɪɴ"},
        {"id": FORCE_SUB_CHANNEL2, "name": "Jᴏɪɴ"},
        {"id": FORCE_SUB_CHANNEL3, "name": "Jᴏɪɴ"}
    ]

    # Check if the user is subscribed to any of the channels
    subscribed_to_channel = False
    buttons = []

    # Add buttons for all channels
    for channel in force_sub_channels:
        try:
            if bool(JOIN_REQUEST_ENABLE):
                invite = await client.create_chat_invite_link(
                    chat_id=channel["id"],
                    creates_join_request=True
                )
                ButtonUrl = invite.invite_link
            else:
                ButtonUrl = client.invitelink  # If JOIN_REQUEST_ENABLE is disabled

            # Attempt to check if the user is a member of the current channel
            member = await client.get_chat_member(chat_id=channel["id"], user_id=message.from_user.id)
            if member.status in ["member", "administrator", "owner"]:
                subscribed_to_channel = True  # User is subscribed to this channel

            # Create a button for the channel
            buttons.append(
                [InlineKeyboardButton(f"Join {channel['name']}", url=ButtonUrl)]
            )

        except Exception as e:
            # Handle errors (e.g., if the user is not subscribed or other issues)
            pass

    # If the user is not subscribed to any of the channels, show the buttons to join the channels
    if not subscribed_to_channel:
        try:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="Try Again",
                        url=f"https://t.me/{client.username}?start={message.command[1]}"
                    )
                ]
            )
        except IndexError:
            pass

        await message.reply(
            text=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            quote=True,
            disable_web_page_preview=True
        )

    else:
        # If the user is subscribed to any of the channels, proceed with the normal start behavior
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡️ ᴍᴀɪɴ ʜᴜʙ", url="t.me/Anime_Movies_Hindi_Dub_India"),
                    InlineKeyboardButton("🍁 ᴏᴡɴᴇʀ", url="t.me/Shikamaru_Naru")
                ],
                [
                    InlineKeyboardButton("🛈 ᴀʙᴏᴜᴛ", callback_data = "about"),
                    InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data = "close")
                ]
            ]
        )
        if START_PIC:  # Check if START_PIC has a value
            await message.reply_photo(
                photo=START_PIC,
                caption=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                quote=True
            )
        else:  # If START_PIC is empty, send only the text
            await message.reply_text(
                text=START_MSG.format(
                    first=message.from_user.first_name,
                    last=message.from_user.last_name,
                    username=None if not message.from_user.username else '@' + message.from_user.username,
                    mention=message.from_user.mention,
                    id=message.from_user.id
                ),
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                quote=True
            )
        return

    
#=====================================================================================##

WAIT_MSG = """"<b>Pʀᴏᴄᴇssɪɴɢ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

