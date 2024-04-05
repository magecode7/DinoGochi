from bot.exec import bot
from typing import Optional
from time import time
from asyncio import sleep
from bot.modules.logs import log
from bot.modules.data_format import seconds_to_str
from typing import Any, Callable

last_message = 0
col_now = 0

async def send_message():
    return 0

async def antiflood(function: Callable, *args, number_retries=5, **kwargs):
    """
    Use this function inside loops in order to avoid getting TooManyRequests error.
    Example:
    
    .. code-block:: python3
    
        from telebot.util import antiflood
        for chat_id in chat_id_list:
        msg = antiflood(bot.send_message, chat_id, text)
        
    :param function: The function to call
    :type function: :obj:`Callable`

    :param number_retries: Number of retries to send
    :type function: :obj:int

    :param args: The arguments to pass to the function
    :type args: :obj:`tuple`

    :param kwargs: The keyword arguments to pass to the function
    :type kwargs: :obj:`dict`

    :return: None
    """
    from telebot.apihelper import ApiTelegramException
    from time import sleep

    for _ in range(number_retries - 1):
        try:
            return await function(*args, **kwargs)
        except ApiTelegramException as ex:
            if ex.error_code == 429:
                sleep(ex.result_json['parameters']['retry_after'])
            else:
                raise
    else:
        return await function(*args, **kwargs)