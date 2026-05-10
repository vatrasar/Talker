import flet as ft
from dataclasses import dataclass, field

from Features.Landing.Domain.Models.project import Project


@ft.observable
@dataclass
class ProjectPickState:
    """
    State for the ProjectPick screen.

    Used In: ProjectPickViewModel, ProjectPickView.
    """
    projects: list[Project] = field(default_factory=list)
