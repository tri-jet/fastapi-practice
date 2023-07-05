# Remember, CRUD = Create, Read, Update, Delete
# In this case, only doing Create and Read (do Update and Delete as extension)
from sqlalchemy.orm import Session

from . import models, schemas

def get_user(db: Session, user_id: int): # defining types of the database and user_id
    return db.query(models.User).filter(models.User.id == user_id).first()
    # query database in the models schema for the User table, where the one of the rows in the User table has the given user id value.
    # i.e. Select User From Users Where User.id = Given ID (first instance)

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()
    # why define skip and limit as constants within the function parameters?

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_pswd = user.password + "not actually hashed" # here you would actually do = hashfunction(pswd)
    db_user = models.User(email = user.email, hashed_pswd = fake_hashed_pswd) # instantiate User class with arguments
    db.add(db_user) # add instance to db
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Item).offset(skip).limit(limit).all()
    #item_dict = db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_user_item = models.Item(**item.dict(), owner_id = user_id)
    db.add(db_user_item)
    db.commit()
    db.refresh(db_user_item)
    return db_user_item

def get_user_item(db: Session, item_id: int, owner_id: int):
    return db.query(models.Item).filter(models.Item.id ==item_id and models.Item.owner_id == owner_id).first()

def delete_user_item(db: Session, item_id: int, owner_id: int):
    # db_user_item = get_user_item(db=Session, item_id=item_id, owner_id=owner_id)
    # issue is that db_user_item is a query result rather than an item instance/need to find what
    # type of argument db.delete takes.
    # db.delete(db_user_item)
    # db.commit()
    # db.refresh()
    # return None
    db.query(models.Item).filter(models.Item.id == item_id and models.Item.owner_id==owner_id).delete()
    db.commit()

