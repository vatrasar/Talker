import flet as ft
from dataclasses import dataclass, field

from features.landing.domain.models.project import Project


@ft.observable
@dataclass
class ProjectPickState:
    """
    State for the ProjectPick screen.

    Used In: ProjectPickViewModel, ProjectPickView.
    """
    projects: list[Project] = field(default_factory=list)
