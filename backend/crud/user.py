import schema, models
from sqlalchemy.orm import Session

def get_userModel(user: schema.User, db: Session):
    return db.query(models.User).filter(models.User.user_name == user.user_name).first()
    
