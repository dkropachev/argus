import ipaddress
from enum import Enum
from pydantic.dataclasses import dataclass
from pydantic import ValidationError, validator
from argus.db.db_types import ArgusUDTBase


@dataclass(init=True, repr=True)
class CloudInstanceDetails(ArgusUDTBase):
    provider: str = ""
    region: str = ""
    public_ip: str = ""
    private_ip: str = ""
    creation_time: int = 0
    termination_time: int = 0
    termination_reason: str = ""

    @classmethod
    def from_db_udt(cls, udt):
        return cls(provider=udt.provider, region=udt.region, public_ip=udt.public_ip, private_ip=udt.private_ip,
                   creation_time=udt.creation_time, termination_time=udt.termination_time,
                   termination_reason=udt.termination_reason)

    @validator("public_ip")
    def valid_public_ip_address(cls, v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValidationError(f"Not a valid IPv4(v6) address: {v}")

        return v

    @validator("private_ip")
    def valid_private_ip_address(cls, v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValidationError(f"Not a valid IPv4(v6) address: {v}")

        return v


@dataclass(init=True, repr=True)
class CloudNodesInfo(ArgusUDTBase):
    image_id: str
    instance_type: str
    node_amount: int
    post_behaviour: str

    @classmethod
    def from_db_udt(cls, udt):
        return cls(image_id=udt.image_id, instance_type=udt.instance_type,
                   node_amount=udt.node_amount, post_behaviour=udt.post_behaviour)


@dataclass(init=True, repr=True)
class BaseCloudSetupDetails(ArgusUDTBase):
    db_node: CloudNodesInfo
    loader_node: CloudNodesInfo
    monitor_node: CloudNodesInfo
    backend: str = None
    _typename = "CloudSetupDetails"

    @classmethod
    def from_db_udt(cls, udt):
        db_node = CloudNodesInfo(*udt.db_node)
        loader_node = CloudNodesInfo(*udt.loader_node)
        monitor_node = CloudNodesInfo(*udt.monitor_node)
        backend = udt.backend
        return cls(db_node=db_node, loader_node=loader_node, monitor_node=monitor_node, backend=backend)


@dataclass(init=True, repr=True)
class AWSSetupDetails(BaseCloudSetupDetails):
    backend: str = "aws"


@dataclass(init=True, repr=True)
class GCESetupDetails(BaseCloudSetupDetails):
    backend: str = "gce"


class ResourceState(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    TERMINATED = "terminated"


@dataclass(init=True, repr=True)
class CloudResource(ArgusUDTBase):
    name: str
    state: str
    instance_info: CloudInstanceDetails

    @classmethod
    def from_db_udt(cls, udt):
        instance_info = CloudInstanceDetails.from_db_udt(udt.instance_info)
        return cls(name=udt.name, state=udt.state, instance_info=instance_info)

    @validator("state")
    def valid_state(cls, v):
        try:
            ResourceState(v)
        except ValueError:
            raise ValidationError(f"Not a valid resource state: {v}")

        return v

    def terminate(self):
        self.state = ResourceState.TERMINATED

    def stop(self):
        self.state = ResourceState.STOPPED
