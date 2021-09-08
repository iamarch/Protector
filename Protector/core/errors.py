"""Protector Errors Constructor"""
# Protector (A telegram bot project)
# Copyright (C) 2021 - Kunaldiwan All rights reserved. Source code available under the AGPL.

# This file is part of Protector.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__all__ = ["ProtectorException", "BackupError", "CommandInvokeError", "UnknownUpdateError"]


class ProtectorException(Exception):
    """Base exception class for Protector"""


class BackupError(ProtectorException):
    """Unexpected backup data type"""


class CommandInvokeError(ProtectorException):
    """Exception raised when the command being invoked raised an exception.

    Attributes
    origin: (`Exception`):
        The original exception that was raised.
    """

    def __init__(self, err):
        self.origin = err
        super().__init__(f"Command raised an exception: {err.__class__.__name__}: {err}")


class UnknownUpdateError(ProtectorException):
    """Exception that's raised when an unknown update handler passed.

    Attributes
    update: (`str`):
        The update handler that doesn't match the handler type.
    """

    def __init__(self, update=None):
        self.update = update
        super().__init__(
            f'Unknown handler: got "{update}", Expecting ["command", "message", "callbackquery"]'
        )
