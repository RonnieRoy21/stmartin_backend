import os

from dotenv import load_dotenv
from postgrest import APIError
from pydantic import ValidationError
from supabase import SupabaseException, create_client
from supabase_auth import UserResponse,AuthResponse

from custom_response import CustomResponse
from models.Counsellor import CounsellorModel, CounsellorProfile
from models.Events import EventModel
from models.Schedules import ScheduleModel


class SupabaseDatabase:
    def __init__(self):
        load_dotenv()
        __supabaseUrl = os.getenv("supabase_url")
        __supabaseKey = os.getenv("supabase_key")
        if not __supabaseKey or not __supabaseUrl:
            raise ValueError("Database Connection Error")
        self.supabase = create_client(
            supabase_url=__supabaseUrl, supabase_key=__supabaseKey
        )

    def login_user(self,email:str,password:str):
        try:
            res:AuthResponse=self.supabase.auth.sign_in_with_password({'email':email,"password":password})
            if not  res.user :
                raise Exception("Invalid Credentials.")
            if not res.session:
                raise Exception("Session Expired")
            return res.session.access_token
        except SupabaseException:
            raise
        except APIError:
            raise



    def retrieve_user(self, user_access_token: str):
        try:
            if not user_access_token:
                raise ValueError("Token is null")
            user: UserResponse | None = self.supabase.auth.get_user(user_access_token)
            if not user:
                raise ValueError
            user_id = user.user.id
            response = (
                self.supabase.from_("counsellors")
                .select("*")
                .eq(column="id", value=user_id)
                .single()
                .execute()
            )

            if response:
                userData: CounsellorModel = CounsellorModel.model_validate(
                    response.data
                )
                return userData
            raise ValueError
        except SupabaseException :
            raise 
        except APIError:
            raise


    def getAllCounsellorProfiles(self,user_id:str):
        try:
            counsellors:list=self.supabase.from_("counsellors").select("name,email,phone_number,role").neq('id',user_id).execute().data
            return [CounsellorProfile.model_validate(c) for c in counsellors]
        except SupabaseException:
            raise
        except APIError:
            raise



    def getAllSetSchedules(self,):
        try:
            schedules:list=self.supabase.from_("schedules").select("counsellor_id,day,date,time,month,year,is_cancelled,counsellors(name)").order('date').order('month').eq('is_cancelled',False).execute().data
            
            return [ScheduleModel.model_validate(s) for s in schedules]
        except ValidationError:
            raise
        except SupabaseException:
            raise
        except APIError:
            raise

    def uploadEvent(self,e:EventModel):
        try:
            self.supabase.from_("events").insert({
                'name':e.name,
                'date':e.date,
                'venue':e.venue,
                'description':e.descritpion
            }).execute()
            return CustomResponse(message="Event Posted")
        except SupabaseException :
            raise
        except ValidationError :
            raise
        except APIError:
            raise

        