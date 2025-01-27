#
# Copyright (c) 2021 Nitric Technologies Pty Ltd.
#
# This file is part of Nitric Python 3 SDK.
# See https://github.com/nitrictech/python-sdk for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import annotations

import asyncio

from nitric.api.exception import exception_from_grpc_error
from typing import List, Union
from enum import Enum
from grpclib import GRPCError
from nitric.api.queues import QueueRef, Queues
from nitric.application import Nitric
from nitric.utils import new_default_channel
from nitricapi.nitric.resource.v1 import (
    Resource,
    ResourceServiceStub,
    PolicyResource,
    ResourceType,
    Action,
)

from nitric.resources.base import BaseResource


class QueuePermission(Enum):
    """Valid query expression operators."""

    sending = "sending"
    receiving = "receiving"


def _perms_to_actions(permissions: List[Union[QueuePermission, str]]) -> List[Action]:
    permission_actions_map = {
        QueuePermission.sending: [Action.QueueSend, Action.QueueList, Action.QueueDetail],
        QueuePermission.receiving: [Action.QueueReceive, Action.QueueList, Action.QueueDetail],
    }
    # convert strings to the enum value where needed
    perms = [
        permission if isinstance(permission, QueuePermission) else QueuePermission[permission.lower()]
        for permission in permissions
    ]

    return [action for perm in perms for action in permission_actions_map[perm]]


def _to_resource(queue: Queue) -> Resource:
    return Resource(name=queue.name, type=ResourceType.Queue)


class Queue(BaseResource):
    """A queue resource."""

    name: str
    actions: List[Action]

    def __init__(self, name: str):
        """Construct a new queue resource."""
        self.name = name
        self._channel = new_default_channel()
        self._resources_stub = ResourceServiceStub(channel=self._channel)

    async def _register(self):
        try:
            await self._resources_stub.declare(resource=_to_resource(self))
        except GRPCError as grpc_err:
            raise exception_from_grpc_error(grpc_err)

    async def allow(self, permissions: List[Union[QueuePermission, str]]) -> QueueRef:
        """Request the required permissions for this queue."""
        # Ensure registration of the resource is complete before requesting permissions.
        if self._reg is not None:
            await asyncio.wait({self._reg})

        policy = PolicyResource(
            principals=[Resource(type=ResourceType.Function)],
            actions=_perms_to_actions(permissions),
            resources=[_to_resource(self)],
        )
        try:
            await self._resources_stub.declare(policy=policy)
        except GRPCError as grpc_err:
            raise exception_from_grpc_error(grpc_err)

        return Queues().queue(self.name)


def queue(name: str) -> Queue:
    """
    Create and register a queue.

    If a queue has already been registered with the same name, the original reference will be reused.
    """
    return Nitric._create_resource(Queue, name)
