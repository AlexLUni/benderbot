from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


from aiogram.utils.keyboard import InlineKeyboardBuilder
import app.database.requests as rq

# /start таблица

main = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = 'Что ты можешь?'), 
                                      KeyboardButton(text = 'Файлы')],
                                      [KeyboardButton(text = 'Расписание'),
                                      KeyboardButton(text = 'Спикерские')],
                                      [KeyboardButton(text = 'Тренинги'),
                                       KeyboardButton(text = 'Трансляции'),
                                      KeyboardButton(text = 'Полезные ссылки')]], resize_keyboard= True, input_field_placeholder='Выберите пункт меню...')
##
# one_time_keyboard=False
# ПОСТОЯННЫЕ ТАБЛИЦЫ КАТЕГОРИЙ ДЛЯ ПОЛЬЗОВАТЕЛЕЙ PUBLIC
##
public_file_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Файл-видео', callback_data= 'public_file_videos')],
                                                [InlineKeyboardButton(text = 'Книги', callback_data= 'public_file_books')],
                                                [InlineKeyboardButton(text = 'Презентации', callback_data= 'public_file_present')],
                                                [InlineKeyboardButton(text = 'Прочие материалы', callback_data= 'public_file_other')]])    

public_events = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Москва', callback_data= 'public_events_moskva')],
                                                [InlineKeyboardButton(text = 'Санкт-Петербург', callback_data= 'public_events_sankt')]])

##
##
##
## ПОСТОЯННАЯ ТАБЛИЦЫ КАТЕГОРИЙ ДЛЯ ДОБАВЛЕНИЯ В БД PRIVATE_ADD
##
##

private_add_file_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Файл-видео', callback_data= 'private_add_file_videos')],
                                                [InlineKeyboardButton(text = 'Книги', callback_data= 'private_add_file_books')],
                                                [InlineKeyboardButton(text = 'Презентации', callback_data= 'private_add_file_present')],
                                                [InlineKeyboardButton(text = 'Прочие материалы', callback_data= 'private_add_file_other')]])    


private_add_const_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Расписание', callback_data= 'private_add_const_schedule')],
                                                [InlineKeyboardButton(text = 'Полезные ссылки', callback_data= 'private_add_const_links')],
                                                [InlineKeyboardButton(text = 'Контакты', callback_data= 'private_add_const_contacts')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])


private_add_temp_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Cпикерские', callback_data= 'private_add_temp_speakers')],
                                                [InlineKeyboardButton(text = 'Тренинги', callback_data= 'private_add_temp_trainings')],
                                                [InlineKeyboardButton(text = 'Трансляции', callback_data= 'private_add_temp_streams')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])


private_add_event_city = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Онлайн', callback_data= 'private_add_event_city_online')],
                                                [InlineKeyboardButton(text = 'Москва', callback_data= 'private_add_event_city_moskva')],
                                                [InlineKeyboardButton(text = 'Санкт-Петербург', callback_data= 'private_add_event_city_sankt')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])

private_add_event_name = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'НАЗВАНИЯ ОФФЛАЙН ВСТРЕЧ:', callback_data="no_action")],
                                                [InlineKeyboardButton(text = 'Антикафе Good Times', callback_data= 'private_add_event_name_good')],
                                                [InlineKeyboardButton(text = 'Коворкинг Рабочая Неделя', callback_data= 'private_add_event_name_busyweek')],
                                                [InlineKeyboardButton(text = 'НАЗВАНИЯ ОНЛАЙН ВСТРЕЧ:', callback_data="no_action")],
                                                [InlineKeyboardButton(text = 'BrainStorm', callback_data= 'private_add_event_name_brainstorm')],
                                                [InlineKeyboardButton(text = 'JazzCode', callback_data= 'private_add_event_name_jazz')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])


private_add_event_day = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Понедельник', callback_data= 'private_add_event_day_monday')],
                                                [InlineKeyboardButton(text = 'Вторник', callback_data= 'private_add_event_day_tuesday')],
                                                [InlineKeyboardButton(text = 'Среда', callback_data= 'private_add_event_day_wednesday')],
                                                [InlineKeyboardButton(text = 'Четверг', callback_data= 'private_add_event_day_thursday')],
                                                [InlineKeyboardButton(text = 'Пятница', callback_data= 'private_add_event_day_friday')],
                                                [InlineKeyboardButton(text = 'Суббота', callback_data= 'private_add_event_day_saturday')],
                                                [InlineKeyboardButton(text = 'Воскресенье', callback_data= 'private_add_event_day_sunday')],
                                                [InlineKeyboardButton(text = 'Каждый день', callback_data= 'private_add_event_day_daily')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])
##
##
##
##
# ПОСТОЯННЫЕ КАТЕГОРИИ ТАБЛИЦ ДЛЯ УДАЛЕНИЯ PRIVATE_DEL
##
##
##

private_del_file_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Файл-видео', callback_data= 'private_del_file_videos')],
                                                [InlineKeyboardButton(text = 'Книги', callback_data= 'private_del_file_books')],
                                                [InlineKeyboardButton(text = 'Презентации', callback_data= 'private_del_file_present')],
                                                [InlineKeyboardButton(text = 'Бендер', callback_data= 'private_del_file_bender')],
                                                [InlineKeyboardButton(text = 'Прочие материалы', callback_data= 'private_del_file_other')]])   


private_del_const_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Расписание', callback_data= 'private_del_const_schedule')],
                                                [InlineKeyboardButton(text = 'Полезные ссылки', callback_data= 'private_del_const_links')],
                                                [InlineKeyboardButton(text = 'Контакты', callback_data= 'private_del_const_contacts')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])

private_del_temp_categories = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Cпикерские', callback_data= 'private_del_temp_speakers')],
                                                [InlineKeyboardButton(text = 'Тренинги', callback_data= 'private_del_temp_trainings')],
                                                [InlineKeyboardButton(text = 'Трансляции', callback_data= 'private_del_temp_streams')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])

private_del_event_day = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Понедельник', callback_data= 'private_del_event_day_monday')],
                                                [InlineKeyboardButton(text = 'Вторник', callback_data= 'private_del_event_day_tuesday')],
                                                [InlineKeyboardButton(text = 'Среда', callback_data= 'private_del_event_day_wednesday')],
                                                [InlineKeyboardButton(text = 'Четверг', callback_data= 'private_del_event_day_thursday')],
                                                [InlineKeyboardButton(text = 'Пятница', callback_data= 'private_del_event_day_friday')],
                                                [InlineKeyboardButton(text = 'Суббота', callback_data= 'private_del_event_day_saturday')],
                                                [InlineKeyboardButton(text = 'Воскресенье', callback_data= 'private_del_event_day_sunday')],
                                                [InlineKeyboardButton(text = 'Каждый день', callback_data= 'private_del_event_day_daily')],
                                                [InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])
##
# ОТМЕНИТЬ, ЕСЛИ ПЕРЕДУМАЛ ДЕЛАТЬ ЧТО-ТО CANCEL
##
cancel = InlineKeyboardMarkup(inline_keyboard= [[InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel')]])
##
##
##
## ФАЙЛЫ/СООБЩЕНИЯ ВЫБРАННОЙ КАТЕГОРИИ FILE_, TEMP_MES_, CONST_MES_, PRAYER_
##
##
##
async def files_by_category(category):
    all_filenames = await rq.get_files_by_category(category)
    keyboard = InlineKeyboardBuilder()
    for file in all_filenames:
        keyboard.row(InlineKeyboardButton(text=file.name, callback_data=f"file_{file.id}"))
    return keyboard.adjust(1).as_markup()

async def temporary_messages_by_category(category):
        all_temp = await rq.get_temporary_messages_by_category(category)
        array = list(all_temp)
        keyboard = InlineKeyboardBuilder()
        if not array:
             keyboard.row(InlineKeyboardButton(text='Сейчас информации нет.', callback_data="no_action"))
        else:
            for temp_mes in array:
                        keyboard.row(InlineKeyboardButton(text=f"{temp_mes.date} {temp_mes.name}", callback_data=f"temp_mes_{temp_mes.id}"))
        return keyboard.adjust(1).as_markup()


async def constant_messages_by_category(category):
    all_const = await rq.get_constant_messages_by_category(category)
    array = list(all_const)
    keyboard = InlineKeyboardBuilder()
    if not array:
        keyboard.row(InlineKeyboardButton(text='Сейчас информации нет.', callback_data="no_action"))
    else:
        for mes in array:
            keyboard.row(InlineKeyboardButton(text=mes.name, callback_data=f"const_mes_{mes.id}"))
    return keyboard.adjust(1).as_markup()


async def online_events_today(today):
    all_events = await rq.get_event_by_city_and_day('Онлайн', today)
    array = list(all_events)
    keyboard = InlineKeyboardBuilder()
    if not array:
        keyboard.row(InlineKeyboardButton(text='Сегодня онлайн групп нет.', callback_data="no_action"))
    else:
        for event in array:
            keyboard.row(InlineKeyboardButton(text=f"В {event.time} (по мск времени) группа {event.name}", url= f'{event.address}'))
    return keyboard.adjust(1).as_markup()
##
##
##
##  УДАЛИТЬ ФАЙЛЫ/СООБЩЕНИЯ ВЫБРАННОЙ КАТЕГОРИИ DEL
##
##
##

async def files_of_category_to_del(category):
    files = await rq.get_files_by_category(category)
    array = list(files)
    keyboard = InlineKeyboardBuilder()
    if not array:
            keyboard.row(InlineKeyboardButton(text='В этой категории нет файлов', callback_data="no_action"))
    else:           
        for file in array:
            keyboard.row(InlineKeyboardButton(text=file.name, callback_data=f"del_file_{file.id}"))
        keyboard.row(InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel'))
    return keyboard.adjust(1).as_markup()

     

async def delete_temp(user_id, category):
    owner = await rq.from_owner(user_id)
    grandadmin = await rq.from_grandadmin(user_id)
    admin = await rq.from_admin(user_id)
    if owner or grandadmin:
        all_temp = await rq.get_temporary_messages_by_category(category)
    elif admin:
        all_temp = await rq.get_temporary_messages_by_admin_and_category(user_id, category)
    keyboard = InlineKeyboardBuilder()
    array = list(all_temp)
    if not array:
            keyboard.row(InlineKeyboardButton(text='Ты ничего пока не добавил. Попробуй /addtemp', callback_data="no_action"))
    else:
        for temp_mes in array:
            keyboard.row(InlineKeyboardButton(text=f"{temp_mes.date} {temp_mes.name}", callback_data=f"del_temp_mes_{temp_mes.id}"))
        keyboard.row(InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel'))               
    return keyboard.adjust(1).as_markup()

async def delete_const(category):
        all_mes = await rq.get_constant_messages_by_category(category)
        keyboard = InlineKeyboardBuilder()
        array = list(all_mes)
        if not array:
             keyboard.row(InlineKeyboardButton(text='Ты ничего пока не добавил. Попробуй /addconst', callback_data="no_action"))
        else:
            for mes in array:
                keyboard.row(InlineKeyboardButton(text=mes.name, callback_data=f"del_const_mes_{mes.id}"))
            keyboard.row(InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel'))
        return keyboard.adjust(1).as_markup()

async def delete_event(day_schedule):
        all_events = await rq.get_event_by_day(day_schedule)
        keyboard = InlineKeyboardBuilder()
        array = list(all_events)
        if not array:
             keyboard.row(InlineKeyboardButton(text=f'Мероприятий только по {day_schedule} нет, попробуй раздел Каждый День', callback_data="no_action"))
        else:
            for event in array:
                keyboard.row(InlineKeyboardButton(text=f'{event.city} {event.name} в {event.time}', callback_data=f"del_event_{event.id}"))
            keyboard.row(InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel'))
        return keyboard.adjust(1).as_markup()

async def delete_admin(rank):
        all_admins = await rq.get_admins_by_rank(rank)
        keyboard = InlineKeyboardBuilder()
        array = list(all_admins)
        if not array:
             keyboard.row(InlineKeyboardButton(text='Нет администраторов', callback_data="no_action"))
        else:
            for admin in array:
                keyboard.row(InlineKeyboardButton(text=admin.name, callback_data=f"del_admin_{admin.id}"))
            keyboard.row(InlineKeyboardButton(text = 'Ой, стоп отмена', callback_data= 'cancel'))
        return keyboard.adjust(1).as_markup()