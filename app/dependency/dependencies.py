from fastapi import Depends, HTTPException
from app.utils import decode_access_token,oauth2_scheme
from sqlalchemy.orm import Session
from app.models import User
from app.database import connect_db


def get_current_user(
    db: Session = Depends(connect_db), token: str = Depends(oauth2_scheme)
):
    print("token ",token)
    payload = decode_access_token(token=token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token")
    user_id_str = payload.get("sub")
    user_id = int(user_id_str) if user_id_str else None

    if not user_id:
        raise HTTPException(
            status_code=401, detail="Token Missing or User ID is Missing"
        )
    userFound = db.query(User).filter(User.id == user_id).first()
    print("user ",userFound.id)
    if not userFound:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": userFound.id, "email": userFound.email}
