import strawberry
from typing import Optional
from sqlalchemy.orm import Session
from core.config.db import SessionLocal
from models.model import UserModel
from models.model import AddressModel

@strawberry.type
class Address:
    street: Optional[str]
    city: Optional[str]
    zip: Optional[str]


@strawberry.type
class User:
    id: strawberry.ID
    name: Optional[str]
    email: Optional[str]
    address: Optional[Address]

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: strawberry.ID) -> Optional[User]:
        db: Session = SessionLocal()

        user = db.query(UserModel).filter(UserModel.id == int(id)).first()
        if not user:
            return None

        addr = None
        if user.address:
            addr = Address(
                street=user.address.street,
                city=user.address.city,
                zip=user.address.zip
            )

        return User(
            id=user.id,
            name=user.name,
            email=user.email,
            address=addr
        )


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(
        self,
        name: str,
        email: str,
        street: Optional[str] = None,
        city: Optional[str] = None,
        zip: Optional[str] = None
    ) -> User:

        db: Session = SessionLocal()

        new_user = UserModel(
            name=name,
            email=email
        )
        db.add(new_user)
        db.flush()     

        new_addr = AddressModel(
            street=street,
            city=city,
            zip=zip,
            user_id=new_user.id
        )
        db.add(new_addr)
        db.commit()
        db.refresh(new_user)

        return User(
            id=new_user.id,
            name=new_user.name,
            email=new_user.email,
            address=Address(
                street=new_addr.street,
                city=new_addr.city,
                zip=new_addr.zip
            )
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)
