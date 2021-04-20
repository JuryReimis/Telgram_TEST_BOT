from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from keyboards.inline_keyboards.callback_datas import insult_callback, test_callback
from main import dp


@dp.callback_query_handler(insult_callback.filter())
async def give_insult(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=30)
    if callback_data.get("insult_force") == str(1):
        await call.message.answer(text=f"Ну ладно, получай,{call.from_user.first_name}!\nТы разговариваешь, как просроченная колбоса")
    if callback_data.get("insult_force") == str(2):
        await call.message.answer(text=f"Хммм...\nНу ладно. Я думаю, что твое имя- {call.from_user.first_name}, означает отвратительный кожаный ублюдок!")
    if callback_data.get("insult_force") == str(3):
        await call.message.answer(text=f"Ах ты ублюдок кожаный, решил ко мне лезть, говно собачье, да я тебя сам сожру ублюдок вонючий...")


@dp.callback_query_handler(text="cancel")
async def cancel_inline_keyboard(call: CallbackQuery):
    await call.message.answer(text="Сдался...")
    await call.answer(text=f"Ахаха, испугался, кожаный ублюдок, {call.from_user.first_name}!", show_alert=True) #show_alert- сообщение показывается как уведомление на экране
    await call.message.edit_reply_markup() #Закрывает инлайн клавиатуру


@dp.callback_query_handler(test_callback.filter())
async def test(call: CallbackQuery):
    await call.message.answer(text="OK")
    await call.message.edit_reply_markup()
