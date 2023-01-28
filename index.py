from pyrogram import Client, filters
import time
import os

TIME = int(time.time())

async def progress(current, total, mode, reply):
    global TIME
    if int(time.time()) - TIME < 2: return
    try: await reply.edit(f"`{mode} ({current * 100 / total:.1f}%)`")
    except: pass
    TIME = int(time.time())

@Client.on_message(filters.command("rename") & filters.private & filters.reply)
async def rename(client, message):

    # argument check
    if len(message.command) == 1:
        await message.reply_text("New name not found!\ne.g: /rename The Last Of Us")
        return

    reply = await message.reply_text("fetching...")
    document = message.reply_to_message

    # downloading...
    try:
        path = await client.download_media(document, progress=progress, progress_args=('downloading', reply))
    except ValueError:
        await reply.edit("It's not downloadable")
        return

    # uploading with new name
    try:
        file_name = " ".join(message.command[1:]) + "." + path.split(".")[-1]
        await client.send_document(chat_id=message.from_user.id, document=path, file_name=file_name, force_document=True, progress=progress, progress_args=('uploading', reply))
    except Exception as e:
        await reply_edit("Upload failed!")

    # remove reply & document
    try:
        os.remove(path)
        await reply.delete()
    except: pass
        
