import asyncio

from aiogram.utils import executor
from config import dp
import logging
from handlers import client, callback, admin, notification
from data_base.bot_db import sql_create


async def on_startup(_):
    asyncio.create_task(notification.scheduler())
    sql_create()


client.register_handlers_client(dp)
callback.register_handlers_callback(dp)
admin.register_handlers_admin(dp)
#fsm_anketa.register_handlers_fsm_anketa(dp)
notification.register_handlers_notification(dp)

#extra.register_handlers_extra(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)