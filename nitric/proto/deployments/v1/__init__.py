# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: nitric/proto/deployments/v1/deployments.proto
# plugin: python-betterproto
# This file has been @generated
import warnings
from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    AsyncIterator,
    Dict,
    List,
    Optional,
)

import betterproto
import betterproto.lib.google.protobuf as betterproto_lib_google_protobuf
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase

from ...resources import v1 as __resources_v1__
from ...storage import v1 as __storage_v1__


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class ResourceDeploymentAction(betterproto.Enum):
    CREATE = 0
    """A new resource is being created"""

    UPDATE = 1
    """An existing resource is being updated"""

    REPLACE = 2
    """An existing resource is being replaced"""

    SAME = 3
    """No-op on the resource (it already exists and requires no changes)"""

    DELETE = 4
    """An existing resource is being deleted"""


class ResourceDeploymentStatus(betterproto.Enum):
    PENDING = 0
    """The action hasn't started, usually due to a dependency"""

    IN_PROGRESS = 1
    """
    The action in currently in-flight, e.g. waiting for cloud provider to
    provision a resource
    """

    SUCCESS = 2
    """The action has been applied successfully"""

    FAILED = 3
    """The action has failed to be (completely) applied"""


@dataclass(eq=False, repr=False)
class DeploymentUpRequest(betterproto.Message):
    spec: "Spec" = betterproto.message_field(1)
    """The spec to deploy"""

    attributes: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(2)
    """
    A map of attributes related to the deploy request this allows for adding
    project identifiers etc.
    """

    interactive: bool = betterproto.bool_field(3)
    """
    A hint to the provider of the kind of output that the client can accept
    This will allow provider developers to provider richer output back to
    clients.
    """


@dataclass(eq=False, repr=False)
class DeploymentUpEvent(betterproto.Message):
    message: str = betterproto.string_field(1, group="content")
    update: "ResourceUpdate" = betterproto.message_field(2, group="content")
    result: "UpResult" = betterproto.message_field(3, group="content")


@dataclass(eq=False, repr=False)
class ResourceUpdate(betterproto.Message):
    id: "__resources_v1__.ResourceIdentifier" = betterproto.message_field(1)
    """
    The resource being updated, if this is nil the update applies to the stack
    """

    action: "ResourceDeploymentAction" = betterproto.enum_field(3)
    """The type of update being applied"""

    status: "ResourceDeploymentStatus" = betterproto.enum_field(4)
    """The current status of the action being applied"""

    sub_resource: str = betterproto.string_field(5)
    """
    (optional) A globally unique identifier (scoped to the id above), used when
    Nitric Resources map 1:many in a cloud provider. e.g. the container image
    repository for a service deployment. This can also be set when id is nil
    above and it will imply a non-nitric resource that is necessary to deploy
    for a stack to operate  e.g. an Azure StorageAccount
    """

    message: str = betterproto.string_field(6)
    """Additional information about the update"""


@dataclass(eq=False, repr=False)
class UpResult(betterproto.Message):
    """Terminal message indicating deployment success"""

    success: bool = betterproto.bool_field(1)
    """Indicate the success status"""

    text: str = betterproto.string_field(2, group="content")
    """Simple text output as result"""


@dataclass(eq=False, repr=False)
class DeploymentDownRequest(betterproto.Message):
    attributes: "betterproto_lib_google_protobuf.Struct" = betterproto.message_field(1)
    """
    A map of attributes related to the deploy request this allows for adding
    project identifiers etc.
    """

    interactive: bool = betterproto.bool_field(2)
    """
    A hint to the provider of the kind of output that the client can accept
    This will allow provider developers to provider richer output back to
    clients.
    """


@dataclass(eq=False, repr=False)
class DeploymentDownEvent(betterproto.Message):
    message: str = betterproto.string_field(1, group="content")
    result: "DownResult" = betterproto.message_field(2, group="content")
    update: "ResourceUpdate" = betterproto.message_field(3, group="content")


@dataclass(eq=False, repr=False)
class DownResult(betterproto.Message):
    """Terminal message indicating deployment success"""

    pass


@dataclass(eq=False, repr=False)
class ImageSource(betterproto.Message):
    """An image source to be used for service deployment"""

    uri: str = betterproto.string_field(1)
    """
    URI of the docker image To support remote images this may also need to
    provide auth information
    """


@dataclass(eq=False, repr=False)
class Service(betterproto.Message):
    """A unit of compute (i.e. function/container)"""

    image: "ImageSource" = betterproto.message_field(1, group="source")
    """Container image as a service"""

    workers: int = betterproto.int32_field(10)
    """Expected worker count for this service"""

    timeout: int = betterproto.int32_field(11)
    """Configurable timeout for request handling"""

    memory: int = betterproto.int32_field(12)
    """Configurable memory size for this instance"""

    type: str = betterproto.string_field(13)
    """
    A simple type property describes the requested type of service that this
    should be for this project, a provider can implement how this request is
    satisfied in any way
    """

    env: Dict[str, str] = betterproto.map_field(
        14, betterproto.TYPE_STRING, betterproto.TYPE_STRING
    )
    """Environment variables for this service"""

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.is_set("timeout"):
            warnings.warn("Service.timeout is deprecated", DeprecationWarning)
        if self.is_set("memory"):
            warnings.warn("Service.memory is deprecated", DeprecationWarning)


@dataclass(eq=False, repr=False)
class Bucket(betterproto.Message):
    listeners: List["BucketListener"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class BucketListener(betterproto.Message):
    config: "__storage_v1__.RegistrationRequest" = betterproto.message_field(1)
    service: str = betterproto.string_field(2, group="target")
    """The name of an service to target"""


@dataclass(eq=False, repr=False)
class Topic(betterproto.Message):
    subscriptions: List["SubscriptionTarget"] = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Queue(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class KeyValueStore(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class Secret(betterproto.Message):
    pass


@dataclass(eq=False, repr=False)
class SubscriptionTarget(betterproto.Message):
    service: str = betterproto.string_field(1, group="target")
    """The name of an service to target"""


@dataclass(eq=False, repr=False)
class TopicSubscription(betterproto.Message):
    target: "SubscriptionTarget" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class HttpTarget(betterproto.Message):
    service: str = betterproto.string_field(1, group="target")
    """The name of an service to target"""


@dataclass(eq=False, repr=False)
class Http(betterproto.Message):
    """An http proxy resource"""

    target: "HttpTarget" = betterproto.message_field(1)


@dataclass(eq=False, repr=False)
class Api(betterproto.Message):
    openapi: str = betterproto.string_field(1, group="document")
    """
    An OpenAPI document for deployment This document will contain extensions
    that hint of services that should be targeted as part of the deployment
    """


@dataclass(eq=False, repr=False)
class Websocket(betterproto.Message):
    """Declare a new websocket"""

    connect_target: "WebsocketTarget" = betterproto.message_field(1)
    """Target for handling new client connections"""

    disconnect_target: "WebsocketTarget" = betterproto.message_field(2)
    """Target for handling client disconnections"""

    message_target: "WebsocketTarget" = betterproto.message_field(3)
    """Target for handling all other message types"""


@dataclass(eq=False, repr=False)
class WebsocketTarget(betterproto.Message):
    service: str = betterproto.string_field(1, group="target")
    """The name of an service to target"""


@dataclass(eq=False, repr=False)
class ScheduleTarget(betterproto.Message):
    service: str = betterproto.string_field(1, group="target")
    """The name of an service to target"""


@dataclass(eq=False, repr=False)
class Schedule(betterproto.Message):
    target: "ScheduleTarget" = betterproto.message_field(1)
    every: "ScheduleEvery" = betterproto.message_field(10, group="cadence")
    cron: "ScheduleCron" = betterproto.message_field(11, group="cadence")


@dataclass(eq=False, repr=False)
class SqlDatabase(betterproto.Message):
    image_uri: str = betterproto.string_field(1, group="migrations")
    """
    The URI of a docker image to use to execute the migrations for this
    database
    """


@dataclass(eq=False, repr=False)
class ScheduleEvery(betterproto.Message):
    rate: str = betterproto.string_field(1)
    """
    rate string e.g. '5 minutes'. Value frequencies are 'minutes', 'hours',
    'days'.
    """


@dataclass(eq=False, repr=False)
class ScheduleCron(betterproto.Message):
    expression: str = betterproto.string_field(1)
    """standard unix cron expression"""


@dataclass(eq=False, repr=False)
class Resource(betterproto.Message):
    id: "__resources_v1__.ResourceIdentifier" = betterproto.message_field(1)
    service: "Service" = betterproto.message_field(10, group="config")
    bucket: "Bucket" = betterproto.message_field(11, group="config")
    topic: "Topic" = betterproto.message_field(12, group="config")
    api: "Api" = betterproto.message_field(13, group="config")
    policy: "Policy" = betterproto.message_field(14, group="config")
    schedule: "Schedule" = betterproto.message_field(15, group="config")
    key_value_store: "KeyValueStore" = betterproto.message_field(16, group="config")
    secret: "Secret" = betterproto.message_field(17, group="config")
    websocket: "Websocket" = betterproto.message_field(18, group="config")
    http: "Http" = betterproto.message_field(19, group="config")
    queue: "Queue" = betterproto.message_field(20, group="config")
    sql_database: "SqlDatabase" = betterproto.message_field(21, group="config")


@dataclass(eq=False, repr=False)
class Policy(betterproto.Message):
    """
    This is already defined in the resource contracts, unfortunately there are
    parts we don't want to duplicate, such as API config
    """

    principals: List["Resource"] = betterproto.message_field(1)
    actions: List["__resources_v1__.Action"] = betterproto.enum_field(2)
    resources: List["Resource"] = betterproto.message_field(3)


@dataclass(eq=False, repr=False)
class Spec(betterproto.Message):
    resources: List["Resource"] = betterproto.message_field(1)
    """list of resources to deploy"""


class DeploymentStub(betterproto.ServiceStub):
    async def up(
        self,
        deployment_up_request: "DeploymentUpRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> AsyncIterator["DeploymentUpEvent"]:
        async for response in self._unary_stream(
            "/nitric.proto.deployments.v1.Deployment/Up",
            deployment_up_request,
            DeploymentUpEvent,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        ):
            yield response

    async def down(
        self,
        deployment_down_request: "DeploymentDownRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> AsyncIterator["DeploymentDownEvent"]:
        async for response in self._unary_stream(
            "/nitric.proto.deployments.v1.Deployment/Down",
            deployment_down_request,
            DeploymentDownEvent,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        ):
            yield response


class DeploymentBase(ServiceBase):
    async def up(
        self, deployment_up_request: "DeploymentUpRequest"
    ) -> AsyncIterator["DeploymentUpEvent"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
        yield DeploymentUpEvent()

    async def down(
        self, deployment_down_request: "DeploymentDownRequest"
    ) -> AsyncIterator["DeploymentDownEvent"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
        yield DeploymentDownEvent()

    async def __rpc_up(
        self, stream: "grpclib.server.Stream[DeploymentUpRequest, DeploymentUpEvent]"
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.up,
            stream,
            request,
        )

    async def __rpc_down(
        self,
        stream: "grpclib.server.Stream[DeploymentDownRequest, DeploymentDownEvent]",
    ) -> None:
        request = await stream.recv_message()
        await self._call_rpc_handler_server_stream(
            self.down,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/nitric.proto.deployments.v1.Deployment/Up": grpclib.const.Handler(
                self.__rpc_up,
                grpclib.const.Cardinality.UNARY_STREAM,
                DeploymentUpRequest,
                DeploymentUpEvent,
            ),
            "/nitric.proto.deployments.v1.Deployment/Down": grpclib.const.Handler(
                self.__rpc_down,
                grpclib.const.Cardinality.UNARY_STREAM,
                DeploymentDownRequest,
                DeploymentDownEvent,
            ),
        }
