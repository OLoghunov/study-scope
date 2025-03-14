from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600

tokenBlocklist = aioredis.from_url(Config.REDIS_URL)

async def addJtiToBlocklist(jti: str) -> None:
    await tokenBlocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )
    
async def tokenInBlocklist(jti: str) -> bool:
    jti = await tokenBlocklist.get(jti)
    
    return jti is not None