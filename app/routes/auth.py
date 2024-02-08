from fastapi import APIRouter, FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from app.services.supabase_client import get_async_client

app = FastAPI()
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

supabase_client = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.on_event("startup")
async def startup_event():
    global supabase_client
    # Initialize supabase_client asynchronously when the app starts
    # supabase_client = await get_auth_client()
    supabase_client = await get_async_client()


@router.get("/signin/")
async def authenticate(request: Request):
    print("signin")
    redirect_uri = f"{request.base_url}auth/callback"

    # Define the scopes
    scopes = " ".join([
        "user-read-email",
    ])

    response = await supabase_client.auth.sign_in_with_oauth({
        'provider': 'spotify',
        'options': {
            'redirectTo': 'redirect_uri',
            'scopes': scopes
            }
        }
    )

    if not response.url:
        raise HTTPException(status_code=500, detail="Failed to initiate OAuth flow")

    return RedirectResponse(response.url)


@router.get("/signout/")
async def signout():
    print("signout")
    data = await supabase_client.auth.sign_out()
    return data


@router.get("/auth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    error = request.query_params.get("error")

    if error:
        return RedirectResponse(url="/auth/error")  # Redirect to an error page

    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code")

    token_response = await supabase_client.auth.exchange_code_for_token(code,
                                                                        redirect_uri=f"{request.base_url}auth/callback")

    if token_response.error:
        return RedirectResponse(url="/auth/error")  # Redirect to an error page with the error message

    # Here, you might want to set cookies or session tokens based on your authentication flow
    # Since setting cookies directly is different in FastAPI, you'll need to use the response object

    # Redirect to the desired page after successful authentication
    return RedirectResponse(url="/")  # Adjust redirect URL as needed


app.include_router(router)
