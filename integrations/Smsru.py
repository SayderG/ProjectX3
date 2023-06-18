import asyncio

from smsru_api import AsyncSmsRu


class SMSMessages:
    def __init__(self):
        self.api = 'C62049BA-C18F-32E8-4292-73C0830630C7'
        self.sms = AsyncSmsRu(self.api)

    async def check_balance(self):
        balance = await self.sms.balance()
        return balance

    async def check_cost(self, numbers: list, message):
        return await self.sms.cost(*numbers, message=message)

    async def send_message(self, numbers: list, message):
        return await self.sms.send(*numbers, message=message)

    async def limits(self, free: bool = False):
        if free:
            limit = await self.sms.free()
        else:
            limit = await self.sms.limit()
        return limit


SmsApi = SMSMessages()


if __name__ == '__main__':
    print(asyncio.run(SmsApi.check_cost(['89284079200'], message='HAck')))
