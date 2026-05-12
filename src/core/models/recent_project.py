from dataclasses import dataclass
from datetime import datetime


@dataclass
class RecentProject:
    """
    Domain model representing a recently opened project.

    Used In: IRecentProjectRepository, RecentProjectRepository, ProjectPickViewModel.
    """

    id: int
    name: str
    path: str
    last_opened_at: datetime
