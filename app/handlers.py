from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.utils.formatting import Text, Bold
import random, string

import app.database.requests as rq
import app.keyboards as kb

router = Router()
router.message.filter(F.chat.type.in_({'private'}))

class FileEvent(StatesGroup):
    file_id = State()
    file_name = State()
    category = State()

class TempEvent(StatesGroup):
    category = State()
    date = State()
    name = State()
    message = State()

class ConstEvent(StatesGroup):
    category = State()
    name = State() 
    message = State()

class AdminEvent(StatesGroup):
    name = State()
    rank = State() 
    tg_id = State()

class Meeting(StatesGroup):
    city = State()
    name = State()
    day_schedule = State()
    address = State()
    time = State()

###
###
###
###
#PUBLIC COMMANDS:
###
###
###
###
###
#1 NON DATABASE RELATED COMMANDS

@router.message(F.text.lower() == 'привет')
@router.message(CommandStart())
async def cmd_start(message: Message):
    file = await rq.get_bender_file()
    await message.answer_photo(file.file_id)
    await message.answer(f'Привет, {message.from_user.first_name}! Я Бендер, бот-помощник. Напиши команду /help и я расскажу, что умею.', 
                         reply_markup=kb.main)

@router.message(F.text.lower() == 'что ты можешь?')
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(''' 
Напиши мне одну из следующих команд:
/start - открытие меню бота, а также начальная страница
/contacts - контакты поддержки бота
/files - различные файлы (видео, книги, презентации и прочее)
/links - полезные ссылки
/offlineevents - какие встречи сегодня оффлайн
/onlineevents - какие встречи сегодня онлайн
/schedule - расписание еженедельных встреч онлайн и оффлайн
/speakers - спикерские выступления
/streams - трансляции
/trainings - тренинги
/help - инструкция по функциям бота''')

@router.message(Command('checktgid'))
async def checktgid(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}! Вот твой tg_id: {message.from_user.id}')


#2 FILES TABLES COMMANDS

@router.message(F.text.lower() =='файлы')
@router.message(Command('files'))
async def catalog(message: Message):
    await message.answer('Выбери одну из категорий:', reply_markup=kb.public_file_categories)      #Не функции, поэтому не ждем клавиатуры

#3 TEMPORARYMESSAGE TABLE COMMANDS(имеющие дату)

@router.message(F.text.lower() =='спикерские')
@router.message(Command('speakers'))
async def all_speakers(message: Message):
    await message.answer('Вот все предстоящие спикерские:', reply_markup= await kb.temporary_messages_by_category("Спикерские"))

@router.message(F.text.lower() =='трансляции')
@router.message(Command('streams'))
async def all_sessions(message: Message):
    await message.answer('Вот все предстоящие трансляции:', reply_markup= await kb.temporary_messages_by_category("Трансляции"))

@router.message(F.text.lower() =='тренинги')
@router.message(Command('trainings'))
async def all_sessions(message: Message):
    await message.answer('Вот все предстоящие тренинги:', reply_markup= await kb.temporary_messages_by_category("Тренинги"))

#4 CONSTANTMESSAGE TABLE

@router.message(F.text.lower() =='контакты')
@router.message(Command('contacts'))
async def all_contacts(message: Message):
    all_messages = await rq.get_constant_messages_by_category('Контакты')
    for mes in all_messages:
        await message.bot.copy_message(message.chat.id, mes.chat_id, mes.message_id)

@router.message(F.text.lower() =='расписание')
@router.message(Command('schedule'))
async def all_events(message: Message):
    all_messages = await rq.get_constant_messages_by_category('Расписание')
    for mes in all_messages:
        await message.bot.copy_message(message.chat.id, mes.chat_id, mes.message_id)

@router.message(F.text.lower() =='полезные ссылки')
@router.message(Command('links'))
async def all_links(message: Message):
    all_messages = await rq.get_constant_messages_by_category('Полезные ссылки')
    for mes in all_messages:
        await message.bot.copy_message(message.chat.id, mes.chat_id, mes.message_id)


#5 GROUPSTODAY TABLE COMMANDS

@router.message(Command('offlineevents'))
async def liveevents(message: Message):
    await message.answer('Выбери город, в котором хотел бы посмотреть встречи:', reply_markup= kb.public_events)

@router.message(Command('onlineevents'))
async def onlineevents(message: Message):
    day_number = datetime.now().weekday()
    today = ''
    match day_number:
        case 0:
            today = 'Понедельник'
        case 1:
            today = 'Вторник'
        case 2:
            today = 'Среда'
        case 3:
            today = 'Четверг'
        case 4:
            today = 'Пятница'
        case 5:
            today = 'Суббота'
        case 6:
            today = 'Воскресенье'

    await message.answer('Вот все онлайн группы сегодня:', reply_markup= await kb.online_events_today(today))    

###
###        
###
###
###
###
###
###
#PRIVATE COMMANDS
###
###
###
###
###
###
###
###
#1 COMMANDS FOR OWNER ONLY

@router.message(Command('addgrandadmin'))
async def add(message: Message, state: FSMContext):
    owner = await rq.from_owner(message.from_user.id)
    if owner:
        await state.set_state(AdminEvent.name)
        await state.update_data(rank='grandadmin')
        await message.answer('Введи имя администратора:', reply_markup=kb.cancel)

@router.message(AdminEvent.name)
async def register_admin(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AdminEvent.tg_id)
    await message.answer('Введи tg_id администратора:', reply_markup=kb.cancel)

@router.message(AdminEvent.tg_id)
async def register_admin(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    data = await state.get_data()
    await rq.set_admin(data['tg_id'], data['name'], data['rank'])
    await message.answer('Успех! Проверь правильно ли добавил, используй команду /adminlist')
    await state.clear()

@router.message(Command('delgrandadmin'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    if owner:
        await message.answer('Выбери администратора, которого нужно удалить:', reply_markup=await kb.delete_admin('grandadmin'))


#2 COMMANDS FOR GRANDADMINS AND OWNER ONLY
@router.message(F.document)
async def scan_message(message: Message, state: FSMContext):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await state.update_data(file_id = message.document.file_id)
        await state.update_data(file_name = message.document.file_name)
        await state.set_state(FileEvent.category)
        await message.answer('В какую категорию мне добавить этот файл? (P.S. файлы должны уникальные имена)', reply_markup=kb.private_add_file_categories)

@router.message(F.photo)
async def scan_message(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        file_id = message.photo[-1].file_id
        name = ''.join(random.choices(string.ascii_letters + string.digits, k= 8))
        await rq.set_file(file_id, name, 'Бендер')
        await message.answer('Добавил фотографию в категорию Бендер')

@router.message(Command('addadmin'))
async def add(message: Message, state: FSMContext):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await state.set_state(AdminEvent.name)
        await state.update_data(rank='admin')
        await message.answer('Введи имя администратора:', reply_markup=kb.cancel)

@router.message(AdminEvent.name)
async def register_admin(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AdminEvent.tg_id)
    await message.answer('Введи tg_id администратора (если не знаешь, то попроси человека воспользоваться командой /checktgid ):', reply_markup=kb.cancel)

@router.message(AdminEvent.tg_id)
async def register_admin(message: Message, state: FSMContext):
    await state.update_data(tg_id=message.text)
    data = await state.get_data()
    await rq.set_admin(data['tg_id'], data['name'], data['rank'])
    await message.answer('Успех! Проверь правильно ли добавил, используй команду /adminlist')
    await state.clear()

@router.message(Command('addconst'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('Выбери категорию для добавления информации:', reply_markup=kb.private_add_const_categories)

@router.message(ConstEvent.name)
async def register_message(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(ConstEvent.message)
    await message.answer('Введи сообщение, которое нужно сохранить:', reply_markup=kb.cancel)

@router.message(ConstEvent.message)
async def register_message(message: Message, state: FSMContext):
    data = await state.get_data()
    await rq.set_constant_message(message.from_user.id, message.chat.id, message.message_id, data["name"], data["category"])
    await message.answer('''Спасибо! Проверь, все ли правильно указал. Для этого напиши категорию.
                         Чтобы удалить информацию о сообщении - используй /delconst. Чтобы добавить еще используй /addconst''')
    await state.clear()


@router.message(Command('addevent'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('Выбери город встречи (если онлайн, то Онлайн):', reply_markup=kb.private_add_event_city)

@router.message(Meeting.address)
async def register_message(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Meeting.time)
    await message.answer('Напиши время встречи (в формате ЧЧ:ММ 24 часового формата!!!):', reply_markup=kb.cancel)

@router.message(Meeting.time)
async def register_message(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()
    await rq.set_event(message.from_user.id ,data['name'], data['city'], data['address'], data['time'], data['day_schedule'])
    await message.answer('''Спасибо! Успешно сохранил''')
    await state.clear()

@router.message(Command('delconst'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('Выбери категорию сообщения:', reply_markup=kb.private_del_const_categories)


@router.message(Command('deladmin'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('Выбери администратора, которого нужно удалить:', reply_markup=await kb.delete_admin('admin'))

@router.message(Command('delevent'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('В какой день встреча, которую хотел бы удалить?', reply_markup=kb.private_del_event_day)

@router.message(Command('delfile'))
async def add(message: Message):
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
        await message.answer('Какой категори необходимо удалить файл?', reply_markup=kb.private_del_file_categories)

#3 COMMANDS FOR ALL ADMINS

@router.message(Command('admin'))
async def admin_help(message: Message):
    admin = await rq.from_admin(message.from_user.id)
    owner = await rq.from_owner(message.from_user.id)
    grandadmin = await rq.from_grandadmin(message.from_user.id)
    if owner or grandadmin:
                await message.answer('''
    Напиши мне одну из следующих команд:
    /delfile - удалить файл из /files (чтобы добавить - просто отошли файл Бендеру)
    /addtemp - добавить информацию о спикерской, тренинге и т.д.
    /deltemp - удалить информацию о спикерской, тренинге и т.д. (только то, что добавил сам)
    /addconst - добавить информацию о  сообщениях категорий: полезные ссылки, контакты, расписание и т.д.
    /delconst - удалить информацию о сообщениях категорий: полезные ссылки, контакты, расписание и т.д.
    /addevent - добавить информацию для команд /liveevents или /onlineevents
    /delevent - добавить информацию для команд /liveevents или /onlineevents
    /adminlist - список всех администраторов бота
    /addadmin - добавить администратора ранга <<администратор>>
    /deladmin - удалить администратора ранга <<администратор>>
    /checktgid - секретная команда, чтобы узнать свой telegram id                                
    /admin - все доступные приватные функции админов''')
                 
    elif admin:
        await message.answer('''
    Напиши мне одну из следующих команд:
    /addtemp - добавить информацию о спикерской, тренинге и т.д.
    /deltemp - удалить информацию о спикерской, тренинге и т.д. (только то, что добавил сам)
    /adminlist - список всех администраторов бота
    /checktgid - секретная команда, чтобы узнать свой telegram id                     
    /admin - все доступные приватные функции админов''')

@router.message(Command('adminlist'))
async def admin_help(message: Message):
    admin = await rq.from_admin(message.from_user.id)
    owner = await rq.from_owner(message.from_user.id)
    if owner:
        admins = await rq.get_admins()
        for person in admins:
            await message.answer(f'{person.rank} {person.name} {person.tg_id}')
    elif admin:
        admins = await rq.get_admins()
        for person in admins:
            await message.answer(f'{person.rank} {person.name}')

@router.message(Command('addtemp'))
async def add(message: Message, state: FSMContext):
    admin = await rq.from_admin(message.from_user.id)
    if admin:
        await state.set_state(TempEvent.category)
        await message.answer('Выбери категорию для добавления информации:', reply_markup=kb.private_add_temp_categories)

@router.message(TempEvent.date)
async def register_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await state.set_state(TempEvent.name)
    await message.answer('Введи имя того, кто проводит мероприятие. Или название самого мероприятия:', reply_markup=kb.cancel)

@router.message(TempEvent.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(TempEvent.message)
    await message.answer('Введи сообщение про мероприятие для рассылки:', reply_markup=kb.cancel)

@router.message(TempEvent.message)
async def register_message(message: Message, state: FSMContext):
    await state.update_data(message =message.text)
    data = await state.get_data()
    await rq.set_temporary_message(message.from_user.id, message.chat.id, message.message_id, data["date"], data["name"], data["category"])
    await message.answer('''Спасибо! Проверь, все ли правильно указал. Чтобы удалить информацию о сообщении - используй /deltemp. Чтобы добавить еще используй /addtemp''')
    await state.clear()

@router.message(Command('deltemp'))
async def add(message: Message):
    admin = await rq.from_admin(message.from_user.id)
    if admin:
        await message.answer('Выбери категорию сообщения:', reply_markup=kb.private_del_temp_categories)
####
####
####
####
####
####
####
####
#CALLBACKS:
####
####
####
####
####
####
####
####
#1 PUBLIC CATEGORIES CALLBACKS

@router.callback_query(F.data.startswith('public_file_'))
async def file(callback: CallbackQuery):
    sure_name = callback.data.split('_')[2]
    category =''
    match sure_name:
        case 'videos':
            category = 'Файл-видео'
        case 'books':
            category = 'Книги'
        case 'present':
            category = 'Презентации'
        case 'other':
            category = 'Прочие материалы'

    await callback.message.answer(f'{category}:', reply_markup=await kb.files_by_category(category))
    await callback.answer()

@router.callback_query(F.data.startswith('public_events_'))
async def event(callback: CallbackQuery):
    sure_name = callback.data.split('_')[2]
    city =''
    match sure_name:
        case 'moskva':
            city = 'Москва'
        case 'sankt':
            city = 'Санкт-Петербург'
    
    day_number = datetime.now().weekday()
    today = ''
    match day_number:
        case 0:
            today = 'Понедельник'
        case 1:
            today = 'Вторник'
        case 2:
            today = 'Среда'
        case 3:
            today = 'Четверг'
        case 4:
            today = 'Пятница'
        case 5:
            today = 'Суббота'
        case 6:
            today = 'Воскресенье'
    
    all_events = await rq.get_event_by_city_and_day(city, today)
    array = list(all_events)
    if not array:
        await callback.message.answer('Сегодня в этом городе нет мероприятий')
    else:
        city_name = Text(Bold(city), ":")
        await callback.message.answer(**city_name.as_kwargs())
        for event in array:
            mes = Text("В ", Bold(event.time), " (по мск времени) мероприятие ", Bold(event.name), " по адресу: ", event.address)
            await callback.message.answer(**mes.as_kwargs())
    await callback.answer()


#2 SINGLE FILE, PRAYER OR MESSAGE CALLBACK

@router.callback_query(F.data.startswith('file_'))
async def file(callback: CallbackQuery):
    file = await rq.get_file(callback.data.split('_')[1])
    await callback.message.answer_document(file.file_id)
    await callback.answer()

@router.callback_query(F.data.startswith('const_mes_'))
async def constant_message(callback: CallbackQuery):
    mes = await rq.get_constant_message(callback.data.split('_')[2])
    await callback.bot.copy_message(callback.message.chat.id, mes.chat_id, mes.message_id)
    await callback.answer()

@router.callback_query(F.data.startswith('temp_mes_'))
async def temp_message(callback: CallbackQuery):
    mes = await rq.get_temporary_message(callback.data.split('_')[2])
    await callback.bot.copy_message(callback.message.chat.id, mes.chat_id, mes.message_id)
    await callback.answer()



#3 PRIVATE CALLBACKS FOR DELETION (MESSAGES, PRAYERS, ADMINS, FILES)

@router.callback_query(F.data.startswith('del_temp_mes_'))
async def delete_temp(callback: CallbackQuery):
    await rq.delete_temp_message(callback.data.split('_')[3])
    await callback.message.answer('Успешно удалено')
    await callback.answer()

@router.callback_query(F.data.startswith('del_const_mes_'))
async def delete_const(callback: CallbackQuery):
    await rq.delete_const_message(callback.data.split('_')[3])
    await callback.message.answer('Успешно удалено')
    await callback.answer()

@router.callback_query(F.data.startswith('del_admin_'))
async def delete_admin(callback: CallbackQuery):
    await rq.delete_admin(callback.data.split('_')[2])
    await callback.message.answer('Успешно удалено')
    await callback.answer()

@router.callback_query(F.data.startswith('del_event_'))
async def delete_event(callback: CallbackQuery):
    await rq.delete_event(callback.data.split('_')[2])
    await callback.message.answer('Успешно удалено')
    await callback.answer()

@router.callback_query(F.data.startswith('del_file_'))
async def delete_gfile(callback: CallbackQuery):
    await rq.delete_file(callback.data.split('_')[2])
    await callback.message.answer('Успешно удалено')
    await callback.answer()

#4 PRIVATE CALLBACK TO CANCEL CHANGES

@router.callback_query(F.data.startswith('cancel'))
async def cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Понял ничего менять не будем')
    await callback.answer()

#5 PRIVATE CALLBACKS TO ADD LINE IN DB THROUGH KEYBOARD

@router.callback_query(F.data.startswith('private_add_file_'))
async def addfile(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[3]
    category =''
    match sure_name:
        case 'videos':
            category = 'Файл-видео'
        case 'books':
            category = 'Книги'
        case 'present':
            category = 'Презентации'
        case 'other':
            category = 'Прочие материалы'

    await state.update_data(category=category)
    data = await state.get_data()
    await rq.set_file(data['file_id'], data['file_name'], data['category'])
    await callback.message.answer('Успешно добавил твой файл. Воспользуйся командой /files , чтобы проверить')
    await callback.answer()                     

@router.callback_query(F.data.startswith('private_add_const_'))
async def addconst(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[3]
    category =''
    match sure_name:
        case 'schedule':
            category = 'Расписание'
        case 'links':
            category = 'Полезные ссылки'
        case 'contacts':
            category = 'Контакты'
            
    await state.set_state(ConstEvent.name)
    await state.update_data(category=category)
    await callback.message.answer('Напиши название (описание) сообщения. Например: общее расписание', reply_markup=kb.cancel)
    await callback.answer()

@router.callback_query(F.data.startswith('private_add_temp_'))
async def addtemp(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[3]
    category =''
    match sure_name:
        case 'speakers':
            category = 'Спикерские'
        case 'trainings':
            category = 'Тренинги'
        case 'streams':
            category = 'Трансляции'

    await state.set_state(TempEvent.date)
    await state.update_data(category=category)
    await callback.message.answer('Напиши дату события в формате ДД.ММ.ГГГГ:', reply_markup=kb.cancel)
    await callback.answer()

@router.callback_query(F.data.startswith('private_add_event_city_'))
async def city(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[4]
    city =''
    match sure_name:
        case 'online':
            city = 'Онлайн'
        case 'moskva':
            city = 'Москва'
        case 'sankt':
            city = 'Санкт-Петербург'

    await state.set_state(Meeting.name)
    await state.update_data(city=city)
    await callback.message.answer('Выбери название мероприятия', reply_markup=kb.private_add_event_name)
    await callback.answer()

@router.callback_query(F.data.startswith('private_add_event_name_'))
async def name(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[4]
    name =''
    match sure_name:
        case 'good':
            name = 'Антикафе Good Times'
        case 'busyweek':
            name = 'Коворкинг Рабочая Неделя'
        case 'brainstorm':
            name = 'BrainStorm'
        case 'jazz':
            name = 'JazzCode'

    await state.set_state(Meeting.day_schedule)
    await state.update_data(name=name)
    await callback.message.answer('Выбери день мероприятия', reply_markup=kb.private_add_event_day)
    await callback.answer()

@router.callback_query(F.data.startswith('private_add_event_day_'))
async def day(callback: CallbackQuery, state: FSMContext):
    sure_name = callback.data.split('_')[4]
    day =''
    match sure_name:
        case 'monday':
            day = 'Понедельник'
        case 'tuesday':
            day = 'Вторник'
        case 'wednesday':
            day = 'Среда'
        case 'thursday':
            day = 'Четверг'
        case 'friday':
            day = 'Пятница'
        case 'saturday':
            day = 'Суббота'
        case 'sunday':
            day = 'Воскресенье'
        case 'daily':
            day = 'Каждый день'

    await state.set_state(Meeting.address)
    await state.update_data(day_schedule=day)
    await callback.message.answer('Напиши ссылку на группу или физический адрес группы', reply_markup=kb.cancel)
    await callback.answer()


#6 PRIVATE CALLBACKS TO DELETE LINE IN DB THROUGH KEYBOARDS

@router.callback_query(F.data.startswith('private_del_file_'))
async def cancel(callback: CallbackQuery):
    sure_name = callback.data.split('_')[3]
    category =''
    category =''
    match sure_name:
        case 'videos':
            category = 'Файл-видео'
        case 'books':
            category = 'Книги'
        case 'present':
            category = 'Презентации'
        case 'other':
            category = 'Прочие материалы'
        case 'bender':
            category = 'Бендер'


    await callback.message.answer('Выбери файл, который нужно удалить', reply_markup= await kb.files_of_category_to_del(category))
    await callback.answer()

@router.callback_query(F.data.startswith('private_del_const_'))
async def cancel(callback: CallbackQuery):
    sure_name = callback.data.split('_')[3]
    category =''
    match sure_name:
        case 'schedule':
            category = 'Расписание'
        case 'links':
            category = 'Полезные ссылки'
        case 'contacts':
            category = 'Контакты'

    await callback.message.answer('Выбери сообщение, добавленное тобой, которое хотел бы удалить:', reply_markup=await kb.delete_const(category))
    await callback.answer()

@router.callback_query(F.data.startswith('private_del_temp_'))
async def cancel(callback: CallbackQuery):
    sure_name = callback.data.split('_')[3]
    category =''
    match sure_name:
        case 'speakers':
            category = 'Спикерские'
        case 'trainings':
            category = 'Тренинги'
        case 'streams':
            category = 'Трансляции'

    await callback.message.answer('Выбери мероприятие, добавленное тобой, которое хотел бы удалить:', reply_markup=await kb.delete_temp(callback.from_user.id, category))
    await callback.answer()


@router.callback_query(F.data.startswith('private_del_event_day_'))
async def day(callback: CallbackQuery):
    sure_name = callback.data.split('_')[4]
    day =''
    match sure_name:
        case 'monday':
            day = 'Понедельник'
        case 'tuesday':
            day = 'Вторник'
        case 'wednesday':
            day = 'Среда'
        case 'thursday':
            day = 'Четверг'
        case 'friday':
            day = 'Пятница'
        case 'saturday':
            day = 'Суббота'
        case 'sunday':
            day = 'Воскресенье'
        case 'daily':
            day = 'Каждый день'

    await callback.message.answer('Выбери группу для удаления в этот день', reply_markup= await kb.delete_event(day))
    await callback.answer()

