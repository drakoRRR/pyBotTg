from unittest.mock import AsyncMock
import pytest

from buttons import kb_main
from main import get_start
from texts_for_replys import START_TEXT


@pytest.mark.asyncio
async def test_get_start():
    message = AsyncMock()
    await get_start(message)

    message.answer.assert_called_with(text=START_TEXT,
                                      reply_markup=kb_main)


