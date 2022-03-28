from aiogram.dispatcher import Dispatcher
# from aiogram.dispatcher.filters import Text
#
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
# ID = None
#
#
# class FSMAdmin(StatesGroup):
#     photo = State()
#     name = State()
#     description = State()
#     price = State()
#
#
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
# async def make_changes_command(message: types.Message):
#     global ID
#     ID = message.from_user.id
#     await bot.send_message(message.from_user.id, "What do you want, Owner?", reply_markup=admin_kb.kb_admin)
#     await message.delete()
#
#
# # @dp.message_handler(commands='Load', state=None)
# async def cm_start(message: types.Message):
#     # if message.from_user.id == ID:
#     await FSMAdmin.photo.set()
#     await message.reply('Load photo')
#
#
# # @dp.message_handler(state='*', commands='cancel')
# # @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#     await state.finish()
#     await message.reply('OK')
#
#
# # @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
# async def load_photo(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['photo'] = message.photo[0].file_id
#     await FSMAdmin.next()
#     await message.answer('Enter a name:')
#
#
# # @dp.message_handler(state=FSMAdmin.name)
# async def name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await FSMAdmin.next()
#     await message.answer('Enter description')
#
#
# # @dp.message_handler(state=FSMAdmin.description)
# async def description(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['description'] = message.text
#     await FSMAdmin.next()
#     await message.answer('Enter a price:')
#
#
# # @dp.message_handler(state=FSMAdmin.price)
# async def price(message: types.Message, state: FSMContext):
#     await message.answer('YOUR DATA: ')
#     async with state.proxy() as data:
#         data['price'] = float(message.text)
#         await message.answer(str(data))
#     await sqlite_db.sql_add_command(state)
#     await state.finish()
#
#
# # @dp.callback_query_handler(lambda x: x.data and x.data.startswith("del "))
# async def del_callback_run(callback_query: types.CallbackQuery):
#     await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
#     await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} deleted', show_alert=True)

#
# @dp.message_handler(commands='delete')
# async def delete_item(message: types.Message):
#     # if message.from_user.id == ID:
#     read = await sqlite_db.sql_read2(message)
#     for ret in read:
#         await bot.send_photo(message.chat.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\n цена: {ret[3]}',
#                              reply_markup=InlineKeyboardMarkup().add(
#                                  InlineKeyboardButton(f'Delete', callback_data=f'del {ret[1]}')))


def register_handlers_admin(dp: Dispatcher):
    pass
    # dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith("del "))
    #
    # dp.register_message_handler(cm_start, commands=['load'], state=None)
    # dp.register_message_handler(cancel_handler, commands='cancel', state='*')
    # dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')
    # dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    # dp.register_message_handler(name, state=FSMAdmin.name)
    # dp.register_message_handler(description, state=FSMAdmin.description)
    # dp.register_message_handler(price, state=FSMAdmin.price)
