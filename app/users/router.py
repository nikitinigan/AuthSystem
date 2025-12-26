from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, NoDataToUpdateException, UserAlreadyExistsException
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserRegister, SUserUpdate


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router_users.delete("/me")
async def delete_account(current_user=Depends(get_current_user)):

    await UsersDAO.delete(id=current_user.id)
    
    return {
        "status": "deleted",
        "message": "Ваш аккаунт удален",
        "user_id": current_user.id
    }

@router_auth.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        role="user",
    )

@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token", access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router_users.put("/me")
async def update_user_profile(update_data: SUserUpdate, current_user = Depends(get_current_user)):

    update_dict = update_data.model_dump(exclude_unset=True)
    
    if not update_dict:
        raise NoDataToUpdateException
    print(f"Обновление пользователя {current_user.id}: {list(update_dict.keys())}")
    if "email" in update_dict and update_dict["email"] != current_user.email:
        existing_user = await UsersDAO.find_one_or_none(email=update_dict["email"])
        if existing_user:
            raise UserAlreadyExistsException
    await UsersDAO.update(
        filter_by={"id": current_user.id},
        **update_dict
    )
    updated_user = await UsersDAO.find_by_id(current_user.id)
    
    return updated_user