"""Admin check utils"""

from typing import AsyncGenerator, Dict

__all__ = ["adminlist", "user_ban_protected"]


async def adminlist(client, chat_id, full=False) -> AsyncGenerator[Dict, int]:
    """Function to get admin list of a chat.

    Parameters:
        client (`~Protector`):
            Anjani client instance.
        chat_id (`str`, `int`):
            chat id of the requested adminlist.
        full (`bool`):
            Determine the return value
            True -> Returns a generator yielding ChatMember with additional parameters 'name'.
            False -> Returns a generator yielding user_id.
    """
    async for i in client.iter_chat_members(chat_id, filter="administrators"):
        if full:
            if i.user.last_name:
                i.user["name"] = i.user.first_name + i.user.last_name
            else:
                i.user["name"] = i.user.first_name
            yield i
        else:
            yield i.user.id


async def user_ban_protected(bot, chat_id, user_id) -> bool:
    """Return True if user can't be banned"""
    member = await bot.client.get_chat_member(chat_id=chat_id, user_id=user_id)
    return bool(
        member.status in ["creator", "administrator"]
        or user_id in bot.staff_id
        or member.user.id in bot.staff_id
    )
