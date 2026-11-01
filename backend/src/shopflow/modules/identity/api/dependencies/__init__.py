"""Identity API dependencies."""

from typing import Annotated

from fastapi import Depends

from shopflow.core.database.session import get_session
from shopflow.modules.identity.infrastructure.repositories import SqlAlchemyUserRepository


def get_user_repo(session=Depends(get_session)):
    return SqlAlchemyUserRepository(session)


UserRepoDep = Annotated[SqlAlchemyUserRepository, Depends(get_user_repo)]

__all__ = ["get_user_repo", "UserRepoDep"]
