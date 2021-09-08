""" Restriction Plugin. """

from typing import ClassVar

from pyrogram.errors import PeerIdInvalid, UserNotParticipant

from Protector import listener, plugin
from Protector.utils import (
    ParsedChatMember,
    extract_user,
    extract_user_and_text,
    user_ban_protected,
)


class Restrictions(plugin.Plugin):
    name: ClassVar[str] = "Restriction"
    helpable: ClassVar[bool] = True

    async def parse_member(self, user_ids) -> ParsedChatMember:
        """Get member atrribute"""
        member = await extract_user(self.bot.client, user_ids)
        return ParsedChatMember(member)

    @listener.on("kick", can_restrict=True)
    async def kick_member(self, message):
        """Kick chat member"""
        user, _ = extract_user_and_text(message)
        chat_id = message.chat.id
        if user is None:
            return await message.reply_text(await self.bot.text(chat_id, "no-kick-user"))
        try:
            if await user_ban_protected(self.bot, chat_id, user):
                return await message.reply_text(await self.bot.text(chat_id, "admin-kick"))
        except UserNotParticipant:
            return await message.reply_text(await self.bot.text(chat_id, "err-not-participant"))
        await message.chat.kick_member(user)
        kicked = await self.parse_member(user)
        await message.reply_text(await self.bot.text(chat_id, "kick-done", kicked.first_name))
        await message.chat.unban_member(user)

    @listener.on("ban", can_restrict=True)
    async def ban_member(self, message):
        """Ban chat member"""
        user, _ = extract_user_and_text(message)
        chat_id = message.chat.id
        if user is None:
            return await message.reply_text(await self.bot.text(chat_id, "no-ban-user"))
        try:
            if await user_ban_protected(self.bot, chat_id, user):
                return await message.reply_text(await self.bot.text(chat_id, "admin-ban"))
        except UserNotParticipant:
            return await message.reply_text(await self.bot.text(chat_id, "err-not-participant"))
        await message.chat.kick_member(user)
        banned = await self.parse_member(user)
        await message.reply_text(await self.bot.text(chat_id, "ban-done", banned.first_name))

    @listener.on("unban", can_restrict=True)
    async def unban_member(self, message):
        """Unban chat member"""
        (
            user,
            _,
        ) = extract_user_and_text(message)
        if user is None:
            return await message.reply_text(await self.bot.text(message.chat.id, "unban-no-user"))
        try:
            await message.chat.unban_member(user)
        except PeerIdInvalid:
            return await message.reply_text(
                await self.bot.text(message.chat.id, "err-peer-invalid")
            )
        unbanned = await self.parse_member(user)
        await message.reply_text(
            await self.bot.text(message.chat.id, "unban-done", unbanned.first_name)
        )
