import flet as ft
from Features.Landing.Domain.Models.project import Project
from Features.Landing.UI.Screens.ProjectPick.project_pick_state import ProjectPickState


class ProjectPickViewModel:
    """
    ViewModel for the ProjectPick screen.

    Purpose: Handles business logic and state management for project selection.
    Used In: ProjectPickView.
    """

    def __init__(self):
        self.state = ProjectPickState()
        self._load_recent_projects()

    def handle_new_project(self, e: ft.ControlEvent) -> None:
        """
        Handles the action of creating a new project.

        Invoked By: WelcomeHeaderWithNewProject.
        """
        # TODO: Implement new project creation navigation
        pass

    def _load_recent_projects(self) -> None:
        """
        Loads the list of recent projects.
        """
        # Hardcoded data moved from the View
        self.state.projects = [
            Project("AI Marketing Research", "/Users/admin/Documents/Talker/AI-Marketing-Research", "Updated 2h ago"),
            Project("Global Expansion Strategy", "C:\\Projects\\Global-Strategy", "Updated 1d ago"),
            Project("Q3 Financials", "/Volumes/Data/Finance/Q3-2024", "Updated 3d ago"),
            Project("Product Launch Rev 2", "D:\\Work\\Talker\\Launch-Rev2", "Updated 1w ago"),
            Project("Social Media Campaign", "/Users/admin/Projects/Social-Media", "Updated 2w ago"),
            Project("Brand Identity Refresh", "C:\\Designs\\Brand-Refresh", "Updated 3w ago"),
            Project("Market Analysis 2024", "/Volumes/Data/Reports/Market-Analysis", "Updated 1m ago"),
            Project("Investor Pitch Deck", "/Users/admin/Documents/Pitch-Deck", "Updated 2m ago"),
        ]
