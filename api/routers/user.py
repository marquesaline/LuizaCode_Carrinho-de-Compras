from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse

from api.controllers.userController import create_user, get_user_by_email
from api.schemas.user import UserSchema
from api.middlewares.validators import check_email
from api.utils.descriptions import DESCRIPTION_CREATE_USER


router = APIRouter(prefix='/usuarios')

# cadastro de usuário

@router.post('/cadastro', description=DESCRIPTION_CREATE_USER,response_model= UserSchema)
async def createUser(user: UserSchema):

    valid_email = await check_email(user.email)

    if(valid_email):
    
        user_db = await get_user_by_email(email = user.email)
        if(user_db):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={'error': 'Email já cadastrado'}
            )
        
    
        new_user = await create_user(user)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, 
            content= {'Usuário': new_user}
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={'error': 'Email inválido. Informe um email válido'}
    )


# buscar usuário pelo email, o email deve ser passado na query

@router.get('/email', response_model= UserSchema)
async def get_user(email: str):
    
    valid_email = await check_email(email)

    if(valid_email):
        user_db = await get_user_by_email(email)
        
        if(user_db):
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={'Usuário': user_db}
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail= {'error':'Usuário não encontrado'}
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={'error':'Email inválido. Informe um email válido'}
    )

    
   