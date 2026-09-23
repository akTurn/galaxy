import hashlib

from datetime import datetime, timezone

from core.models.relationship import Relationship
from core.identity.application_identity import build_application_identity


def application_relationships(
    process_observations,
    service_observations,
):

    relationships = []

    applications = {}

    application_service_pairs = set()

    process_to_application = {}

    process_to_service = {}

    # --------------------------------
    # 1. Build PID → Process identity
    # --------------------------------

    pid_to_process = {
        observation.data.get("pid"): observation.entity_id
        for observation in process_observations
        if observation.data.get("pid") is not None
    }

    # --------------------------------
    # 2. Build Process → Service map
    # --------------------------------

    for service_observation in service_observations:

        runtime = service_observation.data.get(
            "runtime",
            {}
        )

        main_pid = runtime.get("main_pid")

        if not main_pid:
            continue

        process_entity_id = pid_to_process.get(
            main_pid
        )

        if process_entity_id is None:
            continue

        process_to_service[
            process_entity_id
        ] = service_observation.entity_id

    # --------------------------------
    # 3. Build Applications
    # --------------------------------

    for process_observation in process_observations:

        data = process_observation.data

        executable = data.get("executable")
        command_line = data.get("command_line")

        if not executable:
            continue

        if isinstance(command_line, list):

            command_line_text = " ".join(
                command_line
            )

        else:

            command_line_text = str(
                command_line or ""
            )

        # --------------------------------
        # Application identity
        # --------------------------------

        # application_identity = (
        #     f"{executable}|{command_line_text}"
        # )
       
        # application_hash = hashlib.sha256(
        #     application_identity.encode("utf-8")
        # ).hexdigest()[:16]
        
        #application_entity_id = application_hash

        application_entity_id = build_application_identity(data)



        # --------------------------------
        # Process → Application map
        # --------------------------------

        process_to_application[
            process_observation.entity_id
        ] = application_entity_id

        # --------------------------------
        # Store application metadata
        # --------------------------------

        applications.setdefault(
            application_entity_id,
            {
                "executable": executable,
                "command_line": command_line,
            },
        )

        # --------------------------------
        # Application → Process
        # --------------------------------

        relationships.append(
            Relationship(
                source_entity_type="application",
                source_entity_id=application_entity_id,
                relationship_type="runs",
                target_entity_type="process",
                target_entity_id=process_observation.entity_id,
                timestamp=process_observation.timestamp,
            )
        )

    # --------------------------------
    # 4. Application → Service
    # --------------------------------

    for process_entity_id, application_entity_id in (
        process_to_application.items()
    ):

        service_entity_id = process_to_service.get(
            process_entity_id
        )

        if service_entity_id is None:
            continue

        pair = (
            application_entity_id,
            service_entity_id,
        )

        if pair in application_service_pairs:
            continue

        application_service_pairs.add(pair)

        relationships.append(
            Relationship(
                source_entity_type="application",
                source_entity_id=application_entity_id,
                relationship_type="associated_with",
                target_entity_type="service",
                target_entity_id=service_entity_id,
                timestamp=datetime.now(timezone.utc),
            )
        )

    return applications, relationships



# PROCESS OBSERVATIONS
#         │
#         ├── PID → Process
#         │
#         ├── Process → Service
#         │
#         └── Process → Application
#                     │
#                     ├── Application → Process
#                     │
#                     └── Application → Service