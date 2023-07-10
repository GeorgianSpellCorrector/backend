import httpx

from app.utils.uvicorn_logger import logger


class HTTPXClientWrapper:
    async_client = None

    def start(self):
        logger.info('starting HTTPX client')
        self.async_client = httpx.AsyncClient()
        logger.info('HTTPX client started')

    async def stop(self):
        logger.info('closing HTTPX client')
        await self.async_client.aclose()
        self.async_client = None
        logger.info('HTTPX client closed')

    def __call__(self):
        assert self.async_client is not None, 'HTTPXClientWrapper not started'
        return self.async_client


httpx_client_wrapper = HTTPXClientWrapper()
