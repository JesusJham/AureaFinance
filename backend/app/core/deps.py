from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Usuario
from app.core.security import SECRET_KEY, ALGORITHM

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = db.query(Usuario).filter(
        Usuario.id == int(user_id)
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )

    return user