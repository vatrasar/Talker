from datetime import datetime, UTC
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from core.data.entities.entity_base import BaseEntity


class RecentProjectEntity(BaseEntity):
    """
    Database entity for storing recent projects information.

    Used In: DBCore (indirectly via registry), RecentProjectRepository.
    """

    __tablename__ = "recent_projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    last_opened_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(UTC), 
        onupdate=lambda: datetime.now(UTC)
    )
