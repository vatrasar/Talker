from dataclasses import dataclass


@dataclass
class Project:
    """
    Represents a user project workspace.

    Used In: RecentProjectCard, ProjectPickViewModel, RecentProjectsList.
    """
    name: str
    path: str
    updated_ago: str
