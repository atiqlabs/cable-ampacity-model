"""Project-management container for IEC 60287 cable ampacity studies.

The project layer organizes studies and their descriptive information.  It is
intentionally independent of engineering calculations, persistence, and GUI
concerns.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from .study import Study


def _utc_now() -> datetime:
    """Return the current timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@dataclass(init=False)
class Project:
    """Organize the studies and descriptive data for one user project.

    ``Project`` is the project-management boundary of the application.  It
    owns the collection of :class:`Study` objects, enforces their unique
    identifiers, and records modification times.  It deliberately does not
    calculate cable ampacity, interpret IEC 60287 rules, persist project data,
    or contain user-interface behavior.

    Attributes:
        project_id: Stable identifier for the project.
        name: User-visible project name.
        description: Optional explanatory text about the project.
        metadata: Application-defined, non-engineering project information.
        created_at: Time at which the project was created, in UTC.
        updated_at: Time at which the project was last modified, in UTC.
    """

    name: str
    description: str
    metadata: dict[str, Any]
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    _studies: list[Study] = field(default_factory=list, init=False, repr=False)

    def __init__(
        self,
        name: str = "Untitled Project",
        description: str = "",
        metadata: Optional[Mapping[str, Any]] = None,
        studies: Optional[Iterable[Study]] = None,
        project_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        """Create a project, optionally with existing studies.

        Args:
            name: User-visible project name.
            description: Optional explanatory project text.
            metadata: Non-engineering, application-defined project data.
            studies: Initial studies to include in the project.
            project_id: Existing identifier when reconstructing a project.
            created_at: Existing creation time when reconstructing a project.
            updated_at: Existing modification time when reconstructing a
                project.

        Raises:
            TypeError: If supplied values have invalid types.
            ValueError: If the name is blank or initial studies have duplicate
                identifiers.
        """
        self.name = self._normalize_name(name, "Project name")
        self.description = self._normalize_description(description)
        self.metadata = self._copy_metadata(metadata)
        self.project_id = project_id if project_id is not None else uuid4()

        timestamp = created_at if created_at is not None else _utc_now()
        self.created_at = timestamp
        self.updated_at = updated_at if updated_at is not None else timestamp
        self._studies = []

        if studies is not None:
            for study in studies:
                self._add_study(study, update_timestamp=False)


        # ------------------------------------------
        # -------PUBLIC INTERFACE -----------------
        #------------------------------------------

        
    @property
    def studies(self) -> tuple[Study, ...]:
        """Return an immutable view of the studies in project order.

        Use :meth:`add_study` and :meth:`remove_study` to modify the project.
        """
        return tuple(self._studies)

    def add_study(self, study: Study) -> None: # add a new study
        """Add a study to the project.

        Args:
            study: Study instance to add.

        Raises:
            TypeError: If ``study`` is not a Study instance.
            ValueError: If another project study has the same identifier.
        """
        self._add_study(study, update_timestamp=True)

    def remove_study(self, study_id: UUID) -> Study:
        """Remove and return the study with the supplied identifier.

        Args:
            study_id: Identifier of the study to remove.

        Returns:
            The removed study.

        Raises:
            KeyError: If no study has ``study_id``.
        """
        for index, study in enumerate(self._studies):
            if study.study_id == study_id:
                self._validate_study(study)
                removed_study = self._studies.pop(index)
                self._touch()
                return removed_study

        raise KeyError(f"No study with ID {study_id} exists in this project.")

    def find_study_by_id(self, study_id: UUID) -> Optional[Study]:
        """Return the study with an identifier, if it belongs to this project.

        Args:
            study_id: Identifier to search for.

        Returns:
            The matching study, or ``None`` when it is not in the project.
        """
        for study in self._studies:
            if study.study_id == study_id:
                return study
        return None

    def find_study_by_name(self, name: str) -> Optional[Study]:
        """Return the first study whose name exactly matches ``name``.

        Args:
            name: Study name to search for.

        Returns:
            The first matching study, or ``None`` when no study matches.

        Raises:
            ValueError: If ``name`` is blank.
        """
        matching_studies = self.find_studies_by_name(name)
        return matching_studies[0] if matching_studies else None

    def find_studies_by_name(self, name: str) -> list[Study]:
        """Return every study whose name exactly matches ``name``.

        Study names are display labels and are not required to be unique.

        Args:
            name: Study name to search for.

        Returns:
            Matching studies in project order.

        Raises:
            ValueError: If ``name`` is blank.
        """
        target_name = self._normalize_name(name, "Study name")
        return [study for study in self._studies if study.name == target_name]

    def get_all_studies(self) -> list[Study]:
        """Return a shallow copy of all studies in project order.

        Returns:
            A list whose mutation cannot add or remove studies from this
            project.
        """
        return list(self._studies)
    
        # - ----------------------------------------------
        # --------PRIVATE HELPERS ------------------------
        # ------------------------------------------------


    def _add_study(self, study: Study, *, update_timestamp: bool) -> None:
        """Validate and store a study, optionally recording the change."""
        self._validate_study(study) # Note already it has been validated, No need for this.
        if self.find_study_by_id(study.study_id) is not None:
            raise ValueError(
                f"A study with ID {study.study_id} already exists in this project."
            )

        self._studies.append(study)
        if update_timestamp:
            self._touch()

    def _touch(self) -> None:
        """Record that project-managed state has changed."""
        self.updated_at = _utc_now()

    @staticmethod
    def _copy_metadata(metadata: Optional[Mapping[str, Any]],) -> dict[str, Any]:
        """Return an owned copy of valid project metadata."""
        if metadata is None:
            return {}
        if not isinstance(metadata, Mapping):
            raise TypeError("metadata must be a mapping.")
        return dict(metadata)

    @staticmethod
    def _normalize_name(name: str, field_name: str) -> str:
        """Validate and normalize a required display name."""
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return name.strip()

    @staticmethod
    def _normalize_description(description: str) -> str:
        """Validate and normalize optional project description text."""
        if not isinstance(description, str):
            raise TypeError("description must be a string.")
        return description.strip()

    @staticmethod
    def _validate_study(study: Study) -> None:
        """Ensure a value is a Study instance.

        Raises:
            TypeError: If ``study`` is not a Study instance.
        """
        if not isinstance(study, Study):
            raise TypeError("study must be an instance of Study.")
