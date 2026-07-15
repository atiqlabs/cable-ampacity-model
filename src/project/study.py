"""Project-management study entity for IEC 60287 engineering cases.

This module intentionally contains no calculation, persistence, or GUI logic.
It groups the engineering input models that define one reproducible study.
"""

from typing import Any, Dict, Mapping, Optional
from uuid import UUID, uuid4

from src.models.cable import Cable
from src.models.environment import Environment
from src.models.installation import Installation


class Study:
    """Represent one self-contained engineering study within a project.

    A study owns the engineering input-model instances for one calculation case.
    The supplied models must not be shared with another study; future study
    duplication workflows are responsible for creating independent copies.
    """

    IEC_60287_AMPACITY = "iec_60287_ampacity"
    SUPPORTED_STUDY_TYPES = (IEC_60287_AMPACITY,)

    def __init__(
        self,
        name: str,
        cable: Cable,
        installation: Installation,
        environment: Environment,
        study_type: str = IEC_60287_AMPACITY,
        metadata: Optional[Mapping[str, Any]] = None,
        study_id: Optional[UUID] = None,
        result_snapshot: Optional[Any] = None,
    ):
        """Create a study with independently owned engineering input models.

        Args:
            name: Editable display name for the engineering case.
            cable: Cable model owned by this study.
            installation: Installation model owned by this study.
            environment: Environment model owned by this study.
            study_type: Identifier for the study calculation/input contract.
            metadata: Optional non-engineering study context and future fields.
            study_id: Existing UUID when reconstructing a known study; otherwise
                a new permanent UUID is generated.
            result_snapshot: Optional non-authoritative derived-result cache.
        """
        if not name or not name.strip():
            raise ValueError("Study name cannot be empty.")

        if study_type not in self.SUPPORTED_STUDY_TYPES:
            raise ValueError(f"Unsupported study type: {study_type}")

        # A UUID is stable internal identity; the editable name is never identity.
        self.study_id = study_id if study_id is not None else uuid4()

        # Study type makes future calculation modules explicit without a class hierarchy.
        self.study_type = study_type
        self.name = name.strip()

        # Copy caller-supplied metadata so the study owns its mutable metadata state.
        self.metadata: Dict[str, Any] = dict(metadata) if metadata is not None else {}

        # These existing engineering models are the authoritative inputs for this case.
        self.cable = cable
        self.installation = installation
        self.environment = environment

        # Snapshots are optional derived data and never replace a fresh calculation.
        self.result_snapshot = result_snapshot
