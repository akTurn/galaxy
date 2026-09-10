import psutil
import socket


from datetime import datetime, timezone

from core.models.observation import Observation


class NetworkCollector:

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
                    "family": str(address.family),
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
           # pid = connection.pid

            if connection.type == socket.SOCK_STREAM:
                protocol = "TCP"

            elif connection.type == socket.SOCK_DGRAM:
                protocol = "UDP"

            else:
                protocol = str(connection.type)

            port_data = {
                "protocol": protocol,
                "address": address,
                "port": port,
                #"pid": pid,
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