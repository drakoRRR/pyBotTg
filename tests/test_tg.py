from unittest.mock import AsyncMock
import pytest

from aiogram.dispatcher import FSMContext
from pyBotTg.buttons import kb_main, close_kb
from pyBotTg.main import get_start, get_descr, get_help, get_audio
from pyBotTg.texts_for_replys import START_TEXT, DESCRIPTION_TEXT, TEXT_HELP


@pytest.mark.asyncio
async def test_get_start():
    message = AsyncMock()
    await get_start(message)

    message.answer.assert_called_with(text=START_TEXT,
                                      reply_markup=kb_main)


@pytest.mark.asyncio
async def test_get_descr():
    message = AsyncMock()
    await get_descr(message)

    message.answer.assert_called_with(text=DESCRIPTION_TEXT)


@pytest.mark.asyncio
async def test_get_help():
    message = AsyncMock()
    await get_help(message)

    message.answer.assert_called_with(text=TEXT_HELP)


@pytest.mark.asyncio
async def test_get_audio():
    message = AsyncMock()
    context = AsyncMock(spec=FSMContext)
    await get_audio(message)

    message.answer.assert_called_with("📍 Надішліть посилання на YouTube відео з аудіо якe хочете завантажити",
                                      reply_markup=close_kb)
    context.set.assert_called_with("Form:WAITING_FOR_MUSIC_TEXT")


