"""Bot rules command"""

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Protector import listener, plugin


class Rules(plugin.Plugin):
    name = "Rules"
    helpable = True

    async def __on_load__(self):
        self.rules_db = self.bot.get_collection("RULES")

    async def __migrate__(self, old_chat, new_chat):
        await self.rules_db.update_one(
            {"chat_id": old_chat},
            {"$set": {"chat_id": new_chat}},
        )

    async def __backup__(self, chat_id, data=None):
        if data and data.get(self.name):
            await self.rules_db.update_one(
                {"chat_id": chat_id}, {"$set": data[self.name]}, upsert=True
            )
        elif not data:
            return await self.rules_db.find_one({"chat_id": chat_id}, {"_id": False})

    @listener.on("setrules", admin_only=True)
    async def set_rules(self, message):
        chat_id = message.chat.id
        if not message.command:
            return await message.reply_text(await self.bot.text(chat_id, "rules-blank-err"))

        content = message.text.markdown.split(None, 1)
        await self.rules_db.update_one(
            {"chat_id": chat_id}, {"$set": {"rules": content[1]}}, upsert=True
        )
        return await message.reply_text(
            await self.bot.text(
                chat_id, "rules-set", f"t.me/{self.bot.username}?start=rules_{chat_id}"
            )
        )

    @listener.on("clearrules", admin_only=True)
    async def clear_rules(self, message):
        chat_id = message.chat.id
        await self.rules_db.delete_one({"chat_id": chat_id})
        await message.reply_text(await self.bot.text(chat_id, "rules-clear"))

    @listener.on("rules")
    async def rules(self, message):
        chat_id = message.chat.id
        content = await self.rules_db.find_one({"chat_id": chat_id})
        if not content:
            return await message.reply_text(await self.bot.text(chat_id, "rules-none"))
        await message.reply_text(
            await self.bot.text(chat_id, "rules-view-caption"),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=await self.bot.text(chat_id, "rules-button"),
                            url=f"t.me/{self.bot.username}?start=rules_{chat_id}",
                        )
                    ]
                ]
            ),
        )
