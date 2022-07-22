"""Active_task."""
from __future__ import annotations

from dataclasses import dataclass

from flask_bpmn.models.db import db
from flask_bpmn.models.db import SpiffworkflowBaseDBModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty

from spiffworkflow_backend.models.principal import PrincipalModel
from spiffworkflow_backend.models.process_instance import ProcessInstanceModel


@dataclass
class ActiveTaskModel(SpiffworkflowBaseDBModel):
    """ActiveTaskModel."""

    __tablename__ = "active_task"
    __table_args__ = (
        db.UniqueConstraint(
            "spiffworkflow_task_id", "process_instance_id", name="active_task_unique"
        ),
    )

    form_json: str | None = ""
    bpmn_json: str = ""
    assigned_principal: RelationshipProperty[PrincipalModel] = relationship(
        PrincipalModel
    )
    id: int = db.Column(db.Integer, primary_key=True)
    spiffworkflow_task_id: str = db.Column(db.String(50), nullable=False)
    process_instance_id: int = db.Column(
        ForeignKey(ProcessInstanceModel.id), nullable=False  # type: ignore
    )
    assigned_principal_id: int = db.Column(ForeignKey(PrincipalModel.id))
    spiffworkflow_task_data: str = db.Column(db.Text)
    status: str = db.Column(db.String(20), nullable=False)
    form_file_name: str | None = db.Column(db.String(50))

    updated_at_in_seconds: int = db.Column(db.Integer)
    created_at_in_seconds: int = db.Column(db.Integer)

    """
    In case of multi-instance, perhaps more than one task may be generated.
    After one task getting completed, the internal variable "Activity_identifier_CurrentVar" will be 
    updated. The variable is shared for all tasks in order to satisfy the completion condition.
    So more active_task records might be related to one active_date record.
    if the above solution is practicable, the save of ActiveTaskModel  will be adjusted later.
    The spiffworkflow_task_data of ActiveTaskModel will be removed either.
    """
    active_data_id: int = db.Column(
        ForeignKey(ActiveDataModel.id), nullable=True
    )