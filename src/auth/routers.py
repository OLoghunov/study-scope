from fastapi import APIRouter


authRouter = APIRouter()

@authRouter.post("/signup")
async def createUserAccount():
    pass