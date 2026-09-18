import psutil
import socket


from datetime import datetime, timezone

from core.models.observation import Observation


class NetworkCollector:


    def _address_family(self, family):

        if family == socket.AF_INET:
            return "IPv4"

        if family == socket.AF_INET6:
            return "IPv6"

        if hasattr(socket, "AF_PACKET") and family == socket.AF_PACKET:
            return "MAC"

        return str(family)


    def collect(self):

        observations = []

        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()
        connections = psutil.net_connections(
                    kind="inet"
                )
        

        for interface_name, addresses in interfaces.items():

            interface_data = {
                "name": interface_name,
                "addresses": [],
            }

            # -------------------------
            # Addresses
            # -------------------------

            for address in addresses:

                interface_data["addresses"].append({
                    #"family": str(address.family),
                    "family": self._address_family(address.family),
                    "address": address.address,
                    "netmask": address.netmask,
                    "broadcast": address.broadcast,
                })

            # -------------------------
            # Interface statistics
            # -------------------------

            interface_stat = stats.get(interface_name)

            if interface_stat:

                interface_data["is_up"] = interface_stat.isup
                interface_data["speed"] = interface_stat.speed
                interface_data["mtu"] = interface_stat.mtu

            # -------------------------
            # Create Observation
            # -------------------------

            observation = Observation(
                source="network",
                entity_type="network_interface",
                entity_id=f"interface:{interface_name}",
                timestamp=datetime.now(timezone.utc),
                data=interface_data,
            )

            observations.append(observation)



        # -------------------------
        # Listening ports
        # -------------------------

        
        for connection in connections:

#             We take the connections and keep only:

#            connection.status == psutil.CONN_LISTEN

            if connection.status != psutil.CONN_LISTEN:
                continue

            if not connection.laddr:
                continue

            address = connection.laddr.ip
            port = connection.laddr.port
            pid = connection.pid

            if connection.type == socket.SOCK_STREAM:
                protocol = "TCP"

            elif connection.type == socket.SOCK_DGRAM:
                protocol = "UDP"

            else:
                protocol = str(connection.type)

            port_data = {
                "protocol": protocol,
                "local_address": address,
                "local_port": port,
                "pid": pid,
                "status": connection.status,
            }

            observation = Observation(
                source="network",
                entity_type="listening_port",
                entity_id=f"{protocol}:{address}:{port}",
                timestamp=datetime.now(timezone.utc),
                data=port_data,
            )

            observations.append(observation)


        # -------------------------
        # Network connections
        # -------------------------

        for connection in connections:

            if not connection.laddr:
                continue

            if not connection.raddr:
                continue

            local_address = connection.laddr.ip
            local_port = connection.laddr.port

            remote_address = connection.raddr.ip
            remote_port = connection.raddr.port

            if connection.type == socket.SOCK_STREAM:
                protocol = "TCP"

            elif connection.type == socket.SOCK_DGRAM:
                protocol = "UDP"

            else:
                protocol = str(connection.type)

            connection_data = {
                "protocol": protocol,
                "local_address": local_address,
                "local_port": local_port,
                "remote_address": remote_address,
                "remote_port": remote_port,
                "state": connection.status,
                "pid": connection.pid,
            }

            observation = Observation(
                source="network",
                entity_type="network_connection",
                entity_id=(
                    f"{protocol}:"
                    f"{local_address}:{local_port}-"
                    f"{remote_address}:{remote_port}"
                ),
                timestamp=datetime.now(timezone.utc),
                data=connection_data,
            )

            observations.append(observation)


        return observations



#     #######/*****Yes — you spotted an important architectural inconsistency.

#  Your **SystemCollector**, **ProcessCollector**, and **NetworkCollector** actually have the same _outer structure_. The difference is that the **data inside each Observation** is different because they represent different kinds of entities.

#  ## The common structure

#  All three ultimately do this:

# ```
# Collector
#    ↓
# list[Observation]
#    ↓
# Observation(
#     source=...,
#     entity_type=...,
#     entity_id=...,
#     timestamp=...,
#     data={...}
# )
# ```

#  Your model is:

# ```
# @dataclass
# class Observation:
#     source: str
#     entity_type: str
#     entity_id: str
#     timestamp: datetime
#     data: dict
# ```

#  So this is consistent.

#  ### System

#  You create **one host observation**:

# ```
# Observation(
#     source="system",
#     entity_type="host",
#     entity_id="localhost",
#     timestamp=...,
#     data={
#         "cpu": ...,
#         "memory": ...,
#         "disk": ...,
#         "os": ...,
#         "hostname": ...,
#         "uptime": ...,
#     },
# )
# ```

#  ### Process

#  You create **one observation per process**:

# ```
# Observation(
#     source="process",
#     entity_type="process",
#     entity_id="pid:...",
#     timestamp=...,
#     data={
#         "pid": ...,
#         "name": ...,
#         "cpu_percent": ...,
#         "memory_percent": ...,
#         "status": ...,
#         "username": ...,
#         "parent_pid": ...,
#         "executable": ...,
#         "command_line": ...,
#         "create_time": ...,
#     },
# )
# ```

#  ### Network

#  You create **multiple types of observations** from one collector:

# ```
# NetworkCollector
#        ↓
#        ├── network_interface
#        ├── listening_port
#        └── network_connection
# ```

#  That's the part that looks different.

#  But it's not actually violating your architecture.

#  ## Why NetworkCollector has three types

#  Because `psutil` exposes several different network concepts:

# ```
# Network
# ├── Interfaces
# ├── Listening ports
# └── Connections
# ```

#  Therefore your collector produces:

# ```
# Observation(
#     entity_type="network_interface",
#     ...
# )
# ```

#  then:

# ```
# Observation(
#     entity_type="listening_port",
#     ...
# )
# ```

#  then:

# ```
# Observation(
#     entity_type="network_connection",
#     ...
# )
# ```

#  That's perfectly valid because **`Observation` is your universal envelope**.

#  Think of it like this:

# ```
#                  Observation
#                       │
#           ┌───────────┼───────────┐
#           │           │           │
#         Host       Process      Network
#           │           │           │
#        data={}      data={}      data={}
# ```

#  The `data` dictionary is allowed to contain fields appropriate to that entity.

#  ## But there IS one thing I'd improve

#  Your NetworkCollector currently has:

# ```
# for connection in connections:
#     ...
#     # create listening_port

# for connection in connections:
#     ...
#     # create network_connection
# ```

#  So you're scanning the same `connections` list twice.

#  That's not necessarily wrong, but structurally I'd eventually make NetworkCollector cleaner:

# ```
# NetworkCollector
# │
# ├── collect_interfaces()
# │
# ├── collect_listening_ports()
# │
# └── collect_connections()
# ```

#  and then:

# ```
# def collect(self):
#     observations = []

#     observations.extend(self.collect_interfaces())
#     observations.extend(self.collect_listening_ports())
#     observations.extend(self.collect_connections())

#     return observations
# ```

#  **But don't change that yet.**

#  Your current architecture is working.

#  ### The important rule for Galaxy

#  Keep this invariant:

# ```
# EVERY collector
#         ↓
# list[Observation]
# ```

#  and:

# ```
# EVERY Observation
#         ↓
# source
# entity_type
# entity_id
# timestamp
# data
# ```

#  Then the contents of `data` can differ.

#  That's actually a **good design**, not a problem.

#  So your current architecture is:

# ```
# SystemCollector
#       ↓
# [Observation(host)]

# ProcessCollector
#       ↓
# [Observation(process), Observation(process), ...]

# NetworkCollector
#       ↓
# [
#   Observation(network_interface),
#   Observation(network_interface),
#   Observation(listening_port),
#   Observation(network_connection),
#   ...
# ]
# ```

#  **That is consistent.
# ** The NetworkCollector isn't supposed to have the same data fields as ProcessCollector; it is supposed to use the same **Observation contract**.