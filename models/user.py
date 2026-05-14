import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base


class Role(str, enum.Enum):
    author = "author"
    customer = "customer"

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            lower = value.lower()
            for member in cls:
                if member.name == lower or member.value.lower() == lower:
                    return member
        return super()._missing_(value)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(
        Enum(
            Role,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
            name="role",
        ),
        nullable=False,
    )

    purchases = relationship("Purchase", back_populates="customer", foreign_keys="Purchase.customer_id")
    reviews = relationship("Review", back_populates="customer")