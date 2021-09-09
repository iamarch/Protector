"""Muting bot commands"""

from pyrogram.errors import (
    PeerIdInvalid,
    UserAdminInvalid,
    UsernameInvalid,
    UsernameNotOccupied,
)
from pyrogram.types import ChatPermissions

from Protector import listener, plugin
from Protector.utils import (
    ParsedChatMember,
    extract_time,
    extract_user,
    extract_user_and_text,
    user_ban_protected,
)


class Muting(plugin.Plugin):
    name = "Muting"
    helpable = True

    async def parse_member(self, user_ids) -> ParsedChatMember:
        """Get member atrribute"""
        member = await extract_user(self.bot.client, user_ids)
        return ParsedChatMember(member)

    async def _muter(self, message, user_id, time=0):
        chat_id = message.chat.id
        try:
            member = await message.chat.get_member(user_id)
            if member.can_send_messages is False and time == 0:
                await message.reply_text(await self.bot.text(chat_id, "already-muted"))
                return False
            await self.bot.client.restrict_chat_member(chat_id, user_id, ChatPermissions(), time)
            return True
        except (UsernameInvalid, UsernameNotOccupied, PeerIdInvalid):
            await message.reply_text(await self.bot.text(chat_id, "err-invalid-username-id"))
            return False
        except UserAdminInvalid:
            await message.reply_text(await self.bot.text(chat_id, "cant-mute-admin"))
            return False

    @listener.on("mute", can_restrict=True)
    async def mute(self, message):
        """Mute chat member"""
        chat_id = message.chat.id
        user_id, res = extract_user_and_text(message)
        if not user_id:
            return await message.reply_text(await self.bot.text(chat_id, "no-mute-user"))
        if user_id in [self.bot.identifier, f"@{self.bot.username}"]:
            return await message.reply_text(await self.bot.text(chat_id, "self-muting"))
        if await user_ban_protected(self.bot, chat_id, user_id):
            return await message.reply_text(await self.bot.text(chat_id, "cant-mute-admin"))

        if res:
            timeflag = res.split(None, 1)[0].lower()
            until = await extract_time(timeflag)
            if not until:
                return await message.reply_text(await self.bot.text(chat_id, "invalid-time-flag"))
            tr_string = "mute-success-time"
        else:
            timeflag = None
            tr_string = "mute-success"
            until = 0
        muted = await self._muter(message, user_id, until)
        if muted:
            member = (await self.parse_member(user_id)).first_name
            await message.reply_text(await self.bot.text(chat_id, tr_string, member, timeflag))

    @listener.on("unmute", can_restrict=True)
    async def unmute(self, message):
        """Unmute chat member"""
        user, _ = extract_user_and_text(message)
        if user is None:
            return await message.reply_text(await self.bot.text(message.chat.id, "no-mute-user"))
        member = await message.chat.get_member(user)
        if member.can_send_messages is False:
            await message.chat.unban_member(user)
            await message.reply_text(await self.bot.text(message.chat.id, "unmute-done"))
        else:
            await message.reply_text(await self.bot.text(message.chat.id, "user-not-muted"))
