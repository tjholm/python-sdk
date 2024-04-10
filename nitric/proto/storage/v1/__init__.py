# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: nitric/proto/storage/v1/storage.proto
# plugin: python-betterproto
# This file has been @generated

from dataclasses import dataclass
from datetime import timedelta
from typing import (
    TYPE_CHECKING,
    AsyncIterable,
    AsyncIterator,
    Dict,
    Iterable,
    List,
    Optional,
    Union,
)

import betterproto
import grpclib
from betterproto.grpc.grpclib_server import ServiceBase


if TYPE_CHECKING:
    import grpclib.server
    from betterproto.grpc.grpclib_client import MetadataLike
    from grpclib.metadata import Deadline


class BlobEventType(betterproto.Enum):
    Created = 0
    Deleted = 1


class StoragePreSignUrlRequestOperation(betterproto.Enum):
    """Operation"""

    READ = 0
    WRITE = 1


@dataclass(eq=False, repr=False)
class ClientMessage(betterproto.Message):
    """ClientMessages are sent from the service to the nitric server"""

    id: str = betterproto.string_field(1)
    """globally unique ID of the request/response pair"""

    registration_request: "RegistrationRequest" = betterproto.message_field(
        2, group="content"
    )
    """Watch for changes on a bucket"""

    blob_event_response: "BlobEventResponse" = betterproto.message_field(
        3, group="content"
    )
    """Response to a blob event (change to a blob)"""


@dataclass(eq=False, repr=False)
class ServerMessage(betterproto.Message):
    """ServerMessages are sent from the nitric server to the service"""

    id: str = betterproto.string_field(1)
    """globally unique ID of the request/response pair"""

    registration_response: "RegistrationResponse" = betterproto.message_field(
        2, group="content"
    )
    """Watch for changes on a bucket"""

    blob_event_request: "BlobEventRequest" = betterproto.message_field(
        3, group="content"
    )
    """Event for a blob in a bucket"""


@dataclass(eq=False, repr=False)
class BlobEventRequest(betterproto.Message):
    bucket_name: str = betterproto.string_field(1)
    blob_event: "BlobEvent" = betterproto.message_field(10, group="event")


@dataclass(eq=False, repr=False)
class BlobEvent(betterproto.Message):
    key: str = betterproto.string_field(1)
    """The key of the blob the event is for"""

    type: "BlobEventType" = betterproto.enum_field(2)
    """The type of event that occurred"""


@dataclass(eq=False, repr=False)
class BlobEventResponse(betterproto.Message):
    success: bool = betterproto.bool_field(1)


@dataclass(eq=False, repr=False)
class RegistrationRequest(betterproto.Message):
    bucket_name: str = betterproto.string_field(1)
    """Name of the bucket to watch"""

    blob_event_type: "BlobEventType" = betterproto.enum_field(2)
    """Event type to listen for"""

    key_prefix_filter: str = betterproto.string_field(3)
    """A blob key prefix to filter events by"""


@dataclass(eq=False, repr=False)
class RegistrationResponse(betterproto.Message):
    id: str = betterproto.string_field(1)
    """The ID of the registration"""


@dataclass(eq=False, repr=False)
class StorageWriteRequest(betterproto.Message):
    """Request to put (create/update) a storage item"""

    bucket_name: str = betterproto.string_field(1)
    """
    Nitric name of the bucket to store in  this will be automatically resolved
    to the provider specific bucket identifier.
    """

    key: str = betterproto.string_field(2)
    """Key to store the item under"""

    body: bytes = betterproto.bytes_field(3)
    """bytes array to store"""


@dataclass(eq=False, repr=False)
class StorageWriteResponse(betterproto.Message):
    """Result of putting a storage item"""

    pass


@dataclass(eq=False, repr=False)
class StorageReadRequest(betterproto.Message):
    """Request to retrieve a storage item"""

    bucket_name: str = betterproto.string_field(1)
    """
    Nitric name of the bucket to retrieve from  this will be automatically
    resolved to the provider specific bucket identifier.
    """

    key: str = betterproto.string_field(2)
    """Key of item to retrieve"""


@dataclass(eq=False, repr=False)
class StorageReadResponse(betterproto.Message):
    """Returned storage item"""

    body: bytes = betterproto.bytes_field(1)
    """The body bytes of the retrieved storage item"""


@dataclass(eq=False, repr=False)
class StorageDeleteRequest(betterproto.Message):
    """Request to delete a storage item"""

    bucket_name: str = betterproto.string_field(1)
    """Name of the bucket to delete from"""

    key: str = betterproto.string_field(2)
    """Key of item to delete"""


@dataclass(eq=False, repr=False)
class StorageDeleteResponse(betterproto.Message):
    """Result of deleting a storage item"""

    pass


@dataclass(eq=False, repr=False)
class StoragePreSignUrlRequest(betterproto.Message):
    """
    Request to generate a pre-signed URL for a blob to perform a specific
    operation, such as read or write.
    """

    bucket_name: str = betterproto.string_field(1)
    """
    Nitric name of the bucket to retrieve from  this will be automatically
    resolved to the provider specific bucket identifier.
    """

    key: str = betterproto.string_field(2)
    """
    Key of item to generate the signed URL for. The URL and the token it
    contains will only be valid for operations on this resource specifically.
    """

    operation: "StoragePreSignUrlRequestOperation" = betterproto.enum_field(3)
    expiry: timedelta = betterproto.message_field(4)
    """Expiry defined as as protobuf duration"""


@dataclass(eq=False, repr=False)
class StoragePreSignUrlResponse(betterproto.Message):
    url: str = betterproto.string_field(1)
    """
    The pre-signed url, restricted to the operation, resource and expiry time
    specified in the request.
    """


@dataclass(eq=False, repr=False)
class StorageListBlobsRequest(betterproto.Message):
    bucket_name: str = betterproto.string_field(1)
    prefix: str = betterproto.string_field(2)


@dataclass(eq=False, repr=False)
class Blob(betterproto.Message):
    key: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class StorageListBlobsResponse(betterproto.Message):
    blobs: List["Blob"] = betterproto.message_field(1)
    """keys of the blobs in the bucket"""


@dataclass(eq=False, repr=False)
class StorageExistsRequest(betterproto.Message):
    bucket_name: str = betterproto.string_field(1)
    key: str = betterproto.string_field(2)
    """Key of item to retrieve"""


@dataclass(eq=False, repr=False)
class StorageExistsResponse(betterproto.Message):
    exists: bool = betterproto.bool_field(1)


class StorageStub(betterproto.ServiceStub):
    async def read(
        self,
        storage_read_request: "StorageReadRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StorageReadResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/Read",
            storage_read_request,
            StorageReadResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def write(
        self,
        storage_write_request: "StorageWriteRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StorageWriteResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/Write",
            storage_write_request,
            StorageWriteResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def delete(
        self,
        storage_delete_request: "StorageDeleteRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StorageDeleteResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/Delete",
            storage_delete_request,
            StorageDeleteResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def pre_sign_url(
        self,
        storage_pre_sign_url_request: "StoragePreSignUrlRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StoragePreSignUrlResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/PreSignUrl",
            storage_pre_sign_url_request,
            StoragePreSignUrlResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def list_blobs(
        self,
        storage_list_blobs_request: "StorageListBlobsRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StorageListBlobsResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/ListBlobs",
            storage_list_blobs_request,
            StorageListBlobsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )

    async def exists(
        self,
        storage_exists_request: "StorageExistsRequest",
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> "StorageExistsResponse":
        return await self._unary_unary(
            "/nitric.proto.storage.v1.Storage/Exists",
            storage_exists_request,
            StorageExistsResponse,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        )


class StorageListenerStub(betterproto.ServiceStub):
    async def listen(
        self,
        client_message_iterator: Union[
            AsyncIterable["ClientMessage"], Iterable["ClientMessage"]
        ],
        *,
        timeout: Optional[float] = None,
        deadline: Optional["Deadline"] = None,
        metadata: Optional["MetadataLike"] = None
    ) -> AsyncIterator["ServerMessage"]:
        async for response in self._stream_stream(
            "/nitric.proto.storage.v1.StorageListener/Listen",
            client_message_iterator,
            ClientMessage,
            ServerMessage,
            timeout=timeout,
            deadline=deadline,
            metadata=metadata,
        ):
            yield response


class StorageBase(ServiceBase):
    async def read(
        self, storage_read_request: "StorageReadRequest"
    ) -> "StorageReadResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def write(
        self, storage_write_request: "StorageWriteRequest"
    ) -> "StorageWriteResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def delete(
        self, storage_delete_request: "StorageDeleteRequest"
    ) -> "StorageDeleteResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def pre_sign_url(
        self, storage_pre_sign_url_request: "StoragePreSignUrlRequest"
    ) -> "StoragePreSignUrlResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def list_blobs(
        self, storage_list_blobs_request: "StorageListBlobsRequest"
    ) -> "StorageListBlobsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def exists(
        self, storage_exists_request: "StorageExistsRequest"
    ) -> "StorageExistsResponse":
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)

    async def __rpc_read(
        self, stream: "grpclib.server.Stream[StorageReadRequest, StorageReadResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.read(request)
        await stream.send_message(response)

    async def __rpc_write(
        self, stream: "grpclib.server.Stream[StorageWriteRequest, StorageWriteResponse]"
    ) -> None:
        request = await stream.recv_message()
        response = await self.write(request)
        await stream.send_message(response)

    async def __rpc_delete(
        self,
        stream: "grpclib.server.Stream[StorageDeleteRequest, StorageDeleteResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.delete(request)
        await stream.send_message(response)

    async def __rpc_pre_sign_url(
        self,
        stream: "grpclib.server.Stream[StoragePreSignUrlRequest, StoragePreSignUrlResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.pre_sign_url(request)
        await stream.send_message(response)

    async def __rpc_list_blobs(
        self,
        stream: "grpclib.server.Stream[StorageListBlobsRequest, StorageListBlobsResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.list_blobs(request)
        await stream.send_message(response)

    async def __rpc_exists(
        self,
        stream: "grpclib.server.Stream[StorageExistsRequest, StorageExistsResponse]",
    ) -> None:
        request = await stream.recv_message()
        response = await self.exists(request)
        await stream.send_message(response)

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/nitric.proto.storage.v1.Storage/Read": grpclib.const.Handler(
                self.__rpc_read,
                grpclib.const.Cardinality.UNARY_UNARY,
                StorageReadRequest,
                StorageReadResponse,
            ),
            "/nitric.proto.storage.v1.Storage/Write": grpclib.const.Handler(
                self.__rpc_write,
                grpclib.const.Cardinality.UNARY_UNARY,
                StorageWriteRequest,
                StorageWriteResponse,
            ),
            "/nitric.proto.storage.v1.Storage/Delete": grpclib.const.Handler(
                self.__rpc_delete,
                grpclib.const.Cardinality.UNARY_UNARY,
                StorageDeleteRequest,
                StorageDeleteResponse,
            ),
            "/nitric.proto.storage.v1.Storage/PreSignUrl": grpclib.const.Handler(
                self.__rpc_pre_sign_url,
                grpclib.const.Cardinality.UNARY_UNARY,
                StoragePreSignUrlRequest,
                StoragePreSignUrlResponse,
            ),
            "/nitric.proto.storage.v1.Storage/ListBlobs": grpclib.const.Handler(
                self.__rpc_list_blobs,
                grpclib.const.Cardinality.UNARY_UNARY,
                StorageListBlobsRequest,
                StorageListBlobsResponse,
            ),
            "/nitric.proto.storage.v1.Storage/Exists": grpclib.const.Handler(
                self.__rpc_exists,
                grpclib.const.Cardinality.UNARY_UNARY,
                StorageExistsRequest,
                StorageExistsResponse,
            ),
        }


class StorageListenerBase(ServiceBase):
    async def listen(
        self, client_message_iterator: AsyncIterator["ClientMessage"]
    ) -> AsyncIterator["ServerMessage"]:
        raise grpclib.GRPCError(grpclib.const.Status.UNIMPLEMENTED)
        yield ServerMessage()

    async def __rpc_listen(
        self, stream: "grpclib.server.Stream[ClientMessage, ServerMessage]"
    ) -> None:
        request = stream.__aiter__()
        await self._call_rpc_handler_server_stream(
            self.listen,
            stream,
            request,
        )

    def __mapping__(self) -> Dict[str, grpclib.const.Handler]:
        return {
            "/nitric.proto.storage.v1.StorageListener/Listen": grpclib.const.Handler(
                self.__rpc_listen,
                grpclib.const.Cardinality.STREAM_STREAM,
                ClientMessage,
                ServerMessage,
            ),
        }