import flet as ft
from abc import ABC, abstractmethod
from typing import Dict, Callable

class BaseFeatureNavigation(ABC):
    """
    Base interface for all feature navigation classes.
    
    This class defines the contract that all feature-specific routing configurations
    must implement to integrate with the central `NavHost`.
    """

    @abstractmethod
    def get_routes(self) -> Dict[str, Callable[[], ft.View]]:
        """
        Retrieves the mapping of route strings to Flet View builder functions.

        Returns:
            Dict[str, Callable[[], ft.View]]: A dictionary where the keys are route
            paths (e.g., "/home") and the values are functions that return an instantiated
            `ft.View` corresponding to that route.
        """
        pass
