#запросы с БД
from app.database.models import async_session
from app.database.models import Admin, File, TemporaryMessage, ConstantMessage, Event
from sqlalchemy import select, and_, or_
from datetime import datetime
import random

# set команды

async def set_admin(tg_id, name, rank):                      #Сохранить админа
    async with async_session() as session:       
        user = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))        

        if not user:
            session.add(Admin(tg_id=tg_id, name = name, rank = rank))
            await session.commit()        
                                         

async def set_file(file_id, file_name, category):    #Сохранить файл
    async with async_session() as session:       
        file = await session.scalar(select(File).where(File.name == file_name))        

        if not file:
            session.add(File(file_id=file_id, name = file_name, category = category))
            await session.commit()        
                                         

async def set_temporary_message(admin_id, chat_id, message_id, date, name, category):
    async with async_session() as session:
        temp_message = await session.scalar(select(TemporaryMessage).where(TemporaryMessage.message_id == message_id and TemporaryMessage.chat_id == chat_id))        

        if not temp_message:
            session.add(TemporaryMessage(admin_id = admin_id, chat_id = chat_id, message_id = message_id, date = date, name = name, category = category))
            await session.commit()

async def set_constant_message(admin_id, chat_id, message_id, name, category):
    async with async_session() as session:
        constant_message = await session.scalar(select(ConstantMessage).where(ConstantMessage.message_id == message_id and ConstantMessage.chat_id == chat_id))        

        if not constant_message:
            session.add(ConstantMessage(admin_id = admin_id, chat_id = chat_id, message_id = message_id, name = name, category = category))
            await session.commit()


async def set_event(admin_id, name, city, address, time, day_schedule):
    async with async_session() as session:
        event = await session.scalar(select(Event).where(and_((Event.name == name), (Event.day_schedule == day_schedule), (Event.time == time))))        

        if not event:
            session.add(Event(admin_id= admin_id,name = name, city = city, address = address, time = time, day_schedule = day_schedule))
            await session.commit()
# get команды
async def get_admins():
    async with async_session() as session:
        return await session.scalars(select(Admin).order_by(Admin.rank))
    
async def get_admins_by_rank(rank):
    async with async_session() as session:
        return await session.scalars(select(Admin).where(Admin.rank == rank).order_by(Admin.name))

async def get_files_by_category(category):
    async with async_session() as session:
        return await session.scalars(select(File).where(File.category == category).order_by(File.name))

async def get_temporary_messages_by_category(category):
    async with async_session() as session:
        return await session.scalars(select(TemporaryMessage).where(TemporaryMessage.category == category).order_by(TemporaryMessage.date))

async def get_constant_messages_by_category(category):
    async with async_session() as session:
        return await session.scalars(select(ConstantMessage).where(ConstantMessage.category == category).order_by(ConstantMessage.name))    

async def get_temporary_messages_by_admin_and_category(user_id, category):
        async with async_session() as session:
            return await session.scalars(select(TemporaryMessage).where(TemporaryMessage.admin_id == user_id and TemporaryMessage.category == category).order_by(TemporaryMessage.date))
        
async def get_event_by_day(day_schedule):
    async with async_session() as session:
        return await session.scalars(select(Event).where(Event.day_schedule == day_schedule).order_by(Event.time)) 

async def get_event_by_city_and_day(city, day_schedule):
    async with async_session() as session:
            return await session.scalars(select(Event).where(and_((Event.city == city), or_((Event.day_schedule == day_schedule), (Event.day_schedule == 'Каждый день'))))
                                         .order_by(Event.time))
        

# Дать юзеру нужный файл или сообщение

async def get_file(file_id):            
    async with async_session() as session:
        return await session.scalar(select(File).where(File.id == file_id))
    
async def get_temporary_message(id):
    async with async_session() as session:
        return await session.scalar(select(TemporaryMessage).where(TemporaryMessage.id == id))
    
async def get_constant_message(id):
    async with async_session() as session:
        return await session.scalar(select(ConstantMessage).where(ConstantMessage.id == id))
    
async def get_event(id):
    async with async_session() as session:
        return await session.scalar(select(Event).where(Event.id == id))
    
async def get_bender_file():
    async with async_session() as session:
        files = await session.scalars(select(File).where(File.category == 'Бендер'))
        array = list(files)
        return random.choice(array)
            

    
# Функции разного характера

async def check_outdated():
    async with async_session() as session:
        today = datetime.now()
        all_temp = await session.scalars(select(TemporaryMessage).order_by(TemporaryMessage.date))
        for temp_message in all_temp:
            day = int(temp_message.date.split('.')[0])
            month = int(temp_message.date.split('.')[1])
            year = int(f"{temp_message.date.split('.')[2]}")
            date = datetime(year, month, day, 22, 30)
            if today > date:
                await session.delete(temp_message)
        await session.commit()

async def from_admin(tg_id):
    async with async_session() as session:
        exists = await session.scalar(select(Admin).where(Admin.tg_id == tg_id))
        if not exists:
            return False
        return True
    
async def from_grandadmin(tg_id):
    async with async_session() as session:
        exists = await session.scalar(select(Admin).where(Admin.tg_id == tg_id and Admin.rank =='grandadmin'))
        if not exists:
            return False
        return True

async def from_owner(tg_id):
    async with async_session() as session:
        exists = await session.scalar(select(Admin).where(Admin.tg_id == tg_id and Admin.rank =='owner'))
        if not exists:
            return False
        return True

#Удаление строк

async def delete_admin(id):                      #Удалить админа
    async with async_session() as session:       
        user = await session.scalar(select(Admin).where(Admin.id == id))        
        if user:
            await session.delete(user)
            await session.commit()        

async def delete_temp_message(id):
    async with async_session() as session:
        temp_message = await session.scalar(select(TemporaryMessage).where(TemporaryMessage.id == id))
        await session.delete(temp_message)
        await session.commit()

async def delete_const_message(id):
    async with async_session() as session:
        const_message = await session.scalar(select(ConstantMessage).where(ConstantMessage.id == id))
        await session.delete(const_message)
        await session.commit()

async def delete_event(id):
    async with async_session() as session:
        event = await session.scalar(select(Event).where(Event.id == id))
        await session.delete(event)
        await session.commit()

async def delete_file(id):
    async with async_session() as session:
        file = await session.scalar(select(File).where(File.id == id))
        await session.delete(file)
        await session.commit()       

