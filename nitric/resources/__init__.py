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
"""Nitric Python SDK API Documentation. See: https://nitric.io/docs?lang=python for full framework documentation."""

from nitric.resources.apis import Api, api
from nitric.resources.buckets import Bucket, bucket
from nitric.resources.collections import Collection, collection
from nitric.resources.queues import Queue, queue
from nitric.resources.schedules import Schedule, schedule
from nitric.resources.secrets import Secret, secret
from nitric.resources.topics import Topic, topic

__all__ = [
    "api",
    "Api",
    "bucket",
    "Bucket",
    "collection",
    "Collection",
    "queue",
    "Queue",
    "Schedule",
    "schedule",
    "secret",
    "Secret",
    "topic",
    "Topic"
]
