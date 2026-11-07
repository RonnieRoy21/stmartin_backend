from fastapi import FastAPI,Depends,HTTPException,status,APIRouter,Request
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from typing import Annotated
from slowapi.util import get_remote_address
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from email_client import EmailClient
from password_generator import PasswordGenerator
from stmartin_supabase import SupabaseDatabase
from starlette.middleware.cors import CORSMiddleware 

app=FastAPI(title="St Martin Admin")
admin_router=APIRouter(prefix="/admin")

async def rate_limit_handler(
    request: Request,
    exc: Exception
):
    if isinstance(exc, RateLimitExceeded):
        return _rate_limit_exceeded_handler(request, exc)

    raise exc

app.add_middleware(
     CORSMiddleware,
     allow_headers=['Authorization'],
     allow_origins=["https://stmartincounsellors.vercel.app"],
     allow_methods=["POST","GET"],
)



limiter=Limiter(key_func=get_remote_address)
app.state.limiter=limiter
app.add_exception_handler(
    RateLimitExceeded,
    rate_limit_handler
)

app.include_router(admin_router)

bearer=HTTPBearer()




def get_db():
    db=SupabaseDatabase()
    yield db

database=Annotated[SupabaseDatabase,Depends(get_db)]

def verify_current_user(db:database,credentials:HTTPAuthorizationCredentials=Depends(bearer)):
    try:
        token=credentials.credentials
        if not token:
            raise HTTPException(detail="Not Authenticated",status_code=status.HTTP_401_UNAUTHORIZED)
        user=db.retrieve_user(user_access_token=token)
        return user.email
    except (TypeError,ValueError,Exception):
        raise HTTPException(detail="UnAuthorized Access",status_code=status.HTTP_403_FORBIDDEN)



verified=Annotated[str,Depends(verify_current_user)]

# ______________Flow_________________

# 1.receive access token and verify user

# 2.checks if userId from access token,if valid, has admin roles from supabase

# 3.if true generate one time password valid for 90 seconds and return it

# 4receive otp for verification and return {role:"",authorized:""}
#
#


@admin_router.get("/verification")
@limiter.limit("10/hour",error_message="Too many requests. Try again after 1 hour")
async def get_verification_code(v:verified,request:Request):
        emailClient=EmailClient()
        emailClient.send_otp_email(recipient_email=v)
        return {
            "message":f"Verification code sent to {v[0]}*****{v.split("@")[0][-1]}@{v.split("@")[1]}.Check your inbox spam folder."
        }


@admin_router.post("/verify-code/{code}")
@limiter.limit("10/hour",error_message="Too many requests. Try again after 1 hour")
async def verify_admin_code(code:str,request:Request):
     try:
        if not code:
               print("No code given" )
               raise HTTPException(
                    detail="Invalid request parameters",
                    status_code=status.HTTP_400_BAD_REQUEST
               )

        gen=PasswordGenerator()
        response=gen.verify_password(code=code)
        return{
             "verified":response
        }
     except Exception:
          raise HTTPException(
               detail="Error Occurred trying to verify code.",
               status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
          )
