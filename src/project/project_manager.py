"""Lifecycle management for the currently active project.

This module deliberately contains no persistence implementation, engineering
calculations, or user-interface code.  Those responsibilities belong to the
repository/serializer, engineering components, and GUI layers respectively.
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .project import Project


class ProjectManager:
    """Manage the lifecycle of the application's current :class:`Project`.

    The manager is a small project-management boundary for callers such as a
    controller.  It owns no engineering state beyond the active project
    reference and intentionally does not perform persistence itself.
    """

    def __init__(self) -> None:
        """Create a manager with no active project."""
        self._current_project: Project | None = None

    def create_new_project(
        self,
        name: str = "Untitled Project",
        *,
        description: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> Project:
        """Create and make active a new project.

        Args:
            name: User-visible project name.
            description: Optional descriptive project text.
            metadata: Optional non-engineering project metadata.

        Returns:
            The newly created active project.

        Raises:
            TypeError: If metadata is not a mapping.
            ValueError: If the project name is blank.
        """
        project = Project(name=name, description=description, metadata=metadata)
        self._current_project = project # make the current project the active project
        return project

    def get_current_project(self) -> Project:
        """Return the active project.

        Raises:
            RuntimeError: If no project is currently active.
        """
        if self._current_project is None:
            raise RuntimeError("No project is currently active.")
        return self._current_project

    def close_current_project(self) -> Project:
        """Close and return the active project without saving it.

        The caller is responsible for any save or unsaved-change decision.

        Raises:
            RuntimeError: If no project is currently active.
        """
        project = self.get_current_project() # save the reference
        self._current_project = None # Remove manager ownership
        return project # return the save reference

    def open_project(self, path: str | Path) -> Project:
        """Load a project from ``path`` when persistence is available.

        This placeholder intentionally does not access the filesystem.  A
        future controller/repository/serializer workflow must only replace the
        active project after a complete, successful load.

        Raises:
            NotImplementedError: Persistence has not been implemented yet.
        """
        del path
        raise NotImplementedError("Project loading is not implemented yet.")

    def save_current_project(self) -> None:
        """Save the active project when persistence is available.

        This placeholder verifies that a project exists but intentionally does
        not serialize data or write files.

        Raises:
            RuntimeError: If no project is currently active.
            NotImplementedError: Persistence has not been implemented yet.
        """
        self.get_current_project()
        raise NotImplementedError("Project saving is not implemented yet.")
