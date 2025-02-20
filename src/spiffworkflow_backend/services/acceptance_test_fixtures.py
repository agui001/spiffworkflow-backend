"""Acceptance_test_fixtures."""
import json
import time

from flask_bpmn.models.db import db

from spiffworkflow_backend.helpers.fixture_data import find_or_create_user
from spiffworkflow_backend.models.process_instance import ProcessInstanceModel
from spiffworkflow_backend.models.process_instance import ProcessInstanceStatus


def load_fixtures() -> list[ProcessInstanceModel]:
    """Load_fixtures."""
    test_process_group_id = "acceptance-tests-group-one"
    test_process_model_id = "acceptance-tests-model-1"
    user = find_or_create_user()
    statuses = ProcessInstanceStatus.list()
    current_time = round(time.time())

    # as of 2022-06-24
    # not_started - 1 hour ago
    # user_input_required - 2 hours ago
    # waiting - 3 hourse ago
    # complete - 4 hours ago
    # faulted - 5 hours ago
    # suspended - 6 hours ago
    process_instances = []
    for i in range(len(statuses)):
        process_instance = ProcessInstanceModel(
            status=statuses[i],
            process_initiator=user,
            process_model_identifier=test_process_model_id,
            process_group_identifier=test_process_group_id,
            updated_at_in_seconds=round(time.time()),
            start_in_seconds=current_time - (3600 * i),
            end_in_seconds=current_time - (3600 * i - 20),
            bpmn_json=json.dumps({"i": i}),
        )
        db.session.add(process_instance)
        process_instances.append(process_instance)

    db.session.commit()
    return process_instances
