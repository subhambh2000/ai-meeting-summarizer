from http import HTTPStatus

from fastapi import HTTPException, APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

from app.auth.schemas import UserOut, SignUpIn, TokenOut
from app.auth.utils import hash_password, verify_password, create_access_token, decode_access_token
from app.services.db_service import get_user_by_username, create_user

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/auth/signup", response_model=UserOut, status_code=201)
async def signup(payload: SignUpIn):
    # check if user already exists
    existing = get_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already taken")

    user_id = create_user(payload.username, hash_password(payload.password))
    if not user_id:
        raise HTTPException(status_code=400, detail="Could not create user")

    return UserOut(id=user_id, username=payload.username)


@router.post("/auth/login", response_model=TokenOut)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers=["WWW-Authenticate", "Bearer"]
        )

    token = create_access_token({"sub": str(user["id"])})
    return token


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid or expired token",
            headers=["WWW-Authenticate", "Bearer"])

    user_id = int(payload["sub"])
    user = get_user_by_username(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut(id=user["id"], username=user["username"])


@router.get("/auth/me", response_model=UserOut)
def read_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
