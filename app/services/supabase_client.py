import os

from supabase_py_async import SupabaseAuthClient, create_client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_ANON_PUBLIC_KEY")

if __name__ == "__main__":
    supabase_auth_client: SupabaseAuthClient = SupabaseAuthClient(url=url)


async def get_async_client():
    return await create_client(url, key)


async def get_auth_client():
    return SupabaseAuthClient(url=url)
