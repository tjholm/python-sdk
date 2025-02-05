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
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, AsyncMock

import pytest
from betterproto.lib.google.protobuf import Struct
from grpclib import GRPCError, Status

from nitric.api import Queues, Task
from nitric.api.exception import UnknownException
from nitric.api.queues import ReceivedTask
from nitricapi.nitric.queue.v1 import (
    QueueReceiveResponse,
    NitricTask,
    QueueCompleteResponse,
    QueueSendBatchResponse,
    FailedTask,
)
from nitric.utils import _struct_from_dict


class Object(object):
    pass


class QueueClientTest(IsolatedAsyncioTestCase):
    async def test_send(self):
        mock_send = AsyncMock()
        mock_response = Object()
        mock_send.return_value = mock_response

        payload = {"content": "of task"}

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send", mock_send):
            queue = Queues().queue("test-queue")
            await queue.send(Task(payload=payload))

        # Check expected values were passed to Stub
        mock_send.assert_called_once()
        assert mock_send.call_args.kwargs["queue"] == "test-queue"
        assert mock_send.call_args.kwargs["task"].id is None
        assert mock_send.call_args.kwargs["task"].payload_type is None
        assert len(mock_send.call_args.kwargs["task"].payload.fields) == 1
        assert mock_send.call_args.kwargs["task"].payload == _struct_from_dict(payload)

    async def test_send_with_failed(self):
        payload = {"content": "of task"}

        mock_send = AsyncMock()
        mock_send.return_value = QueueSendBatchResponse(
            failed_tasks=[
                FailedTask(
                    task=NitricTask(
                        id="test-id",
                        payload=_struct_from_dict(payload),
                    ),
                    message="failed to send in this test",
                )
            ]
        )

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send_batch", mock_send):
            queue = Queues().queue("test-queue")
            failed = await queue.send([Task(payload=payload) for i in range(2)])

        # Check expected values were passed to Stub
        mock_send.assert_called_once()
        self.assertEqual("test-queue", mock_send.call_args.kwargs["queue"])
        assert isinstance(mock_send.call_args.kwargs["tasks"], list)
        # Check that the failed task is returned with its details
        self.assertEqual(1, len(failed))
        self.assertEqual("failed to send in this test", failed[0].message)
        self.assertEqual(payload, failed[0].payload)

    async def test_send_dict(self):
        mock_send = AsyncMock()
        mock_response = Object()
        mock_send.return_value = mock_response

        payload = {"content": "of task"}

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send", mock_send):
            queue = Queues().queue("test-queue")
            await queue.send({"id": "123", "payload": payload})

        # Check expected values were passed to Stub
        mock_send.assert_called_once()
        assert mock_send.call_args.kwargs["queue"] == "test-queue"
        assert mock_send.call_args.kwargs["task"].id == "123"
        assert mock_send.call_args.kwargs["task"].payload_type is None
        assert len(mock_send.call_args.kwargs["task"].payload.fields) == 1
        assert mock_send.call_args.kwargs["task"].payload == _struct_from_dict(payload)

    async def test_send_invalid_type(self):
        mock_send = AsyncMock()
        mock_response = Object()
        mock_send.return_value = mock_response

        payload = {"content": "of task"}

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send", mock_send):
            queue = Queues().queue("test-queue")
            with pytest.raises(AttributeError):
                await queue.send((1, 2, 3))

    async def test_send_none(self):
        mock_send = AsyncMock()
        mock_response = Object()
        mock_send.return_value = mock_response

        payload = {"content": "of task"}

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send", mock_send):
            queue = Queues().queue("test-queue")
            await queue.send()

        # Check expected values were passed to Stub
        mock_send.assert_called_once()
        assert mock_send.call_args.kwargs["queue"] == "test-queue"
        assert mock_send.call_args.kwargs["task"].id is None
        assert mock_send.call_args.kwargs["task"].payload_type is None
        assert mock_send.call_args.kwargs["task"].payload == Struct()

    async def test_send_empty_list(self):
        with pytest.raises(Exception) as e_info:
            await Queues().queue("test-queue").send([])

        self.assertEqual(str(e_info.value), "No tasks provided, nothing to send.")

    async def test_receive(self):
        payload = {"content": "of task"}

        mock_receive = AsyncMock()
        mock_receive.return_value = QueueReceiveResponse(
            tasks=[
                NitricTask(
                    id="test-task", lease_id="test-lease", payload_type="test-type", payload=_struct_from_dict(payload)
                )
            ]
        )

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.receive", mock_receive):
            queueing = Queues()
            queue = queueing.queue("test-queue")
            (task,) = await queue.receive()

        # Check expected values were passed to Stub
        mock_receive.assert_called_once()
        self.assertEqual("test-queue", mock_receive.call_args.kwargs["queue"])
        self.assertEqual(1, mock_receive.call_args.kwargs["depth"])

        self.assertEqual("test-task", task.id)
        self.assertEqual("test-lease", task.lease_id)
        self.assertEqual("test-type", task.payload_type)
        self.assertEqual(payload, task.payload)
        self.assertEqual(queueing, task._queueing)
        self.assertEqual(queue, task._queue)

    async def test_receive_custom_limit(self):
        mock_receive = AsyncMock()
        mock_receive.return_value = QueueReceiveResponse(
            tasks=[
                NitricTask(
                    id="test-task",
                    lease_id="test-lease",
                    payload_type="test-type",
                    payload=_struct_from_dict({"content": "of task"}),
                )
            ]
        )

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.receive", mock_receive):
            await Queues().queue("test-queue").receive(limit=3)  # explicitly set a limit

        # Check expected values were passed to Stub
        mock_receive.assert_called_once()
        self.assertEqual(3, mock_receive.call_args.kwargs["depth"])

    async def test_receive_below_minimum_limit(self):
        mock_receive = AsyncMock()
        mock_receive.return_value = QueueReceiveResponse(
            tasks=[
                NitricTask(
                    id="test-task",
                    lease_id="test-lease",
                    payload_type="test-type",
                    payload=_struct_from_dict({"content": "of task"}),
                )
            ]
        )

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.receive", mock_receive):
            await Queues().queue("test-queue").receive(limit=0)  # explicitly set a limit

        # Check expected values were passed to Stub
        mock_receive.assert_called_once()
        self.assertEqual(1, mock_receive.call_args.kwargs["depth"])

    async def test_receive_task_without_payload(self):
        mock_receive = AsyncMock()
        mock_receive.return_value = QueueReceiveResponse(tasks=[NitricTask(id="test-task", lease_id="test-lease")])

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.receive", mock_receive):
            (task,) = await Queues().queue("test-queue").receive(limit=0)  # explicitly set a limit

        # Verify that an empty dict is returned for payload and no payload type.
        mock_receive.assert_called_once()
        self.assertEqual("", task.payload_type)
        self.assertEqual({}, task.payload)

    async def test_complete(self):
        mock_complete = AsyncMock()
        mock_complete.return_value = QueueCompleteResponse()

        queueing = Queues()
        task = ReceivedTask(lease_id="test-lease", _queueing=queueing, _queue=queueing.queue("test-queue"))

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.complete", mock_complete):
            await task.complete()

        # Check expected values were passed to Stub
        mock_complete.assert_called_once()
        self.assertEqual("test-queue", mock_complete.call_args.kwargs["queue"])
        self.assertEqual("test-lease", mock_complete.call_args.kwargs["lease_id"])

    async def test_complete_task_without_client(self):
        queueing = Queues()
        # lease_id omitted.
        task = ReceivedTask(lease_id="test-lease")

        with pytest.raises(Exception) as e:
            await task.complete()
        self.assertIn("Task is missing internal client", str(e.value))

    async def test_send_error(self):
        mock_send = AsyncMock()
        mock_send.side_effect = GRPCError(Status.UNKNOWN, "test error")

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send", mock_send):
            with pytest.raises(UnknownException) as e:
                await Queues().queue("test-queue").send(Task(payload={"content": "of task"}))

    async def test_send_batch_error(self):
        mock_send = AsyncMock()
        mock_send.side_effect = GRPCError(Status.UNKNOWN, "test error")

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.send_batch", mock_send):
            with pytest.raises(UnknownException) as e:
                await Queues().queue("test-queue").send([Task(payload={"content": "of task"}) for i in range(2)])

    async def test_receive_error(self):
        mock_receive = AsyncMock()
        mock_receive.side_effect = GRPCError(Status.UNKNOWN, "test error")

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.receive", mock_receive):
            with pytest.raises(UnknownException) as e:
                await Queues().queue("test-queue").receive()

    async def test_complete_error(self):
        mock_complete = AsyncMock()
        mock_complete.side_effect = GRPCError(Status.UNKNOWN, "test error")

        queueing = Queues()
        task = ReceivedTask(lease_id="test-lease", _queueing=queueing, _queue=queueing.queue("test-queue"))

        with patch("nitricapi.nitric.queue.v1.QueueServiceStub.complete", mock_complete):
            with pytest.raises(UnknownException) as e:
                await task.complete()
