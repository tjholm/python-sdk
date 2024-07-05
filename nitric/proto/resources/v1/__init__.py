# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: nitric/proto/resources/v1/resources.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Dict,
    List,
    Optional,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class ResourceType(betterproto.Enum):
    Api = 0
    Service = 1
    Bucket = 2
    Topic = 3
    Schedule = 4
    Subscription = 5
    KeyValueStore = 6
    Policy = 7
    Secret = 8
    BucketListener = 9
    Websocket = 10
    Http = 11
    ApiSecurityDefinition = 12
    Queue = 13
    SqlDatabase = 14


class Action(betterproto.Enum):
    BucketFileList = 0
    """Bucket Permissions: 0XX"""

    BucketFileGet = 1
    BucketFilePut = 2
    BucketFileDelete = 3
    TopicPublish = 200
    """Topic Permissions: 2XX"""

    KeyValueStoreRead = 300
    """KeyValue Store Permissions: 3XX"""

    KeyValueStoreWrite = 301
    KeyValueStoreDelete = 302
    SecretPut = 400
    """Secret Permissions: 4XX"""

    SecretAccess = 401
    WebsocketManage = 500
    """Websocket Permissions: 5XX"""

    QueueEnqueue = 600
    """Queue Permissions: 6XX"""

    QueueDequeue = 601


@dataclass(eq=False, repr=False)
class PolicyResource(betterproto.Message):
    principals: List["ResourceIdentifier"] = betterproto.message_field(1)
    actions: List["Action"] = betterproto.enum_field(2)
    resources: List["ResourceIdentifier"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class ResourceIdentifier(betterproto.Message):
    """Unique identifier for a resource within a nitric application."""

    type: "ResourceType" = betterproto.enum_field(1)
    name: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class ResourceDeclareRequest(betterproto.Message):
    id: "ResourceIdentifier" = betterproto.message_field(1)
    policy: "PolicyResource" = betterproto.message_field(10, group="config")
    bucket: "BucketResource" = betterproto.message_field(11, group="config")
    topic: "TopicResource" = betterproto.message_field(12, group="config")
    key_value_store: "KeyValueStoreResource" = betterproto.message_field(
        13, group="config"
    )
    secret: "SecretResource" = betterproto.message_field(14, group="config")
    api: "ApiResource" = betterproto.message_field(15, group="config")
    api_security_definition: "ApiSecurityDefinitionResource" = (
        betterproto.message_field(16, group="config")
    )
    queue: "QueueResource" = betterproto.message_field(17, group="config")
    sql_database: "SqlDatabaseResource" = betterproto.message_field(18, group="config")


@dataclass(eq=False, repr=False)
class BucketResource(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class TopicResource(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class QueueResource(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class KeyValueStoreResource(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class SecretResource(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class SqlDatabaseMigrations(betterproto.Message):
    migrations_path: str = betterproto.string_field(1, group="migrations")
    """
    The path to this databases SQL migrations Valid values are
    file://relative/path/to/migrations as a directory or
    dockerfile://path/to/migrations.dockerfile to hint at a docker image build
    Paths should be relative to the root of the application (nitric.yaml file
    location)
    """


@dataclass(eq=False, repr=False)
class SqlDatabaseResource(betterproto.Message):
    migrations: "SqlDatabaseMigrations" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class ApiOpenIdConnectionDefinition(betterproto.Message):
    issuer: str = betterproto.string_field(1)
    audiences: List[str] = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class ApiSecurityDefinitionResource(betterproto.Message):
    api_name: str = betterproto.string_field(1)
    oidc: "ApiOpenIdConnectionDefinition" = betterproto.message_field(
        2, group="definition"
    )


@dataclass(eq=False, repr=False)
class ApiScopes(betterproto.Message):
    scopes: List[str] = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class ApiResource(betterproto.Message):
    security: Dict[str, "ApiScopes"] = betterproto.map_field(
        1, betterproto.TYPE_STRING, betterproto.TYPE_MESSAGE
    )
    """
    root level security map for this api references
    ApiSecurityDefinitionResource(s)
    """


@dataclass(eq=False, repr=False)
class ResourceDeclareResponse(betterproto.Message):
    pass


class ResourcesStub(betterproto.ServiceStub):
    async def declare(
        self,
        resource_declare_request: "ResourceDeclareRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "ResourceDeclareResponse":
        return await self._unary_unary(
            "/nitric.proto.resources.v1.Resources/Declare",
            resource_declare_request,
            ResourceDeclareResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class ResourcesBase(ServiceBase):
    async def declare(
        self, resource_declare_request: "ResourceDeclareRequest"
    ) -> "ResourceDeclareResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_declare(
        self,
        stream: "grpclib.server.Stream[ResourceDeclareRequest, ResourceDeclareResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.declare(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/nitric.proto.resources.v1.Resources/Declare": grpclib.const.Handler(
                self.__rpc_declare,
                grpclib.const.Cardinality.UNARY_UNARY,
                ResourceDeclareRequest,
                ResourceDeclareResponse,
            ),
        }
