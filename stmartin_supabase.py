import os

from dotenv import load_dotenv
from supabase import SupabaseException, create_client
from supabase_auth import UserResponse

from models.Counsellor import CounsellorModel


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
