from app.database.requests import check_outdated

async def temporary_message_check():    
   await check_outdated()

