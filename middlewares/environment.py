from typing import List
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class EnvironmentMiddleware(LifetimeControllerMiddleware):

    def __init__(self, channel_id):
        super().__init__()
        self.channel_id = channel_id

    async def pre_process(self, obj, data, *args):
        data["channel_id"] = self.channel_id

    async def post_process(self, obj, data, *args):
        pass

