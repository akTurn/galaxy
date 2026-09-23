import hashlib


def build_application_identity(data):

    executable = data.get("executable")

    if not executable:
        executable = data.get("name")

    command_line = data.get("command_line", [])

    if isinstance(command_line, list):
        command_line = " ".join(command_line)

    command_line = str(command_line)

    identity = f"{executable}"

    # only include command line for scripts/interpreters
    if executable in (
        "/usr/bin/python3",
        "/usr/bin/python",
        "/usr/bin/node",
    ):
        identity += f"|{command_line}"

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()[:16]
