import schema, models, auth
from sqlalchemy.orm import Session
from .user import get_userModel
import bcrypt


def create_reflectometer(
        reflectometer : schema.Reflectometer,
        user: schema.User,
        db:Session,
) -> schema.Reflectometer | None:
    user_model = get_userModel(user, db)
    if user_model is None:
        return None
    
    if reflectometer.password is None:
        password_hash = None
        salt = None
    else:
        salt = bcrypt.gensalt().decode()
        password_hash = auth.get_password_hash(reflectometer.password, salt)    

    reflectometer_model = models.Reflectometer(
        owner = user_model.id,
        name = reflectometer.name,
        salt = salt,
        password_hash = password_hash,
    )
    db.add(reflectometer_model)
    db.commit()

    db.refresh(reflectometer_model)
    reflectometer.password = None
    reflectometer.id = reflectometer_model.id

    return reflectometer

def get_reflectometer(
        id : int | None,
        user: schema.User,
        db: Session,
):
    user_model = get_userModel(user, db)
    if user_model is None:
        return None
    
    if id is None:
        return db.query(models.Reflectometer) \
                .filter(models.Reflectometer.owner == user_model.id).all()
    else:
        return db.query(models.Reflectometer) \
                .filter(models.Reflectometer.owner == user_model.id,
                        models.Reflectometer.id == id).all()
    
def delete_reflectometer(
        id : int | None,
        user: schema.User,
        db: Session,
):
    user_model = get_userModel(user, db)
    if user_model is None:
        return None
    db.query(models.Reflectometer) \
        .filter(models.Reflectometer.owner == user_model.id,
                models.Reflectometer.id == id).delete()
    db.commit()
