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
from typing import List, Union
from nitric.faas import ApiWorkerOptions, FunctionServer, HttpMiddleware, Middleware, MethodOptions, HttpMethod
from nitric.application import Nitric
from nitric.resources.base import BaseResource
from nitricapi.nitric.resource.v1 import (
    Resource,
    ResourceType,
    ResourceServiceStub,
    ApiResource,
    ApiScopes,
    ApiSecurityDefinition,
    ApiSecurityDefinitionJwt
)
from nitric.utils import new_default_channel
from grpclib import GRPCError
from nitric.api.exception import exception_from_grpc_error
import importlib


class JwtSecurityDefinition:
    """Represents the JWT security definition for an API."""

    issuer: str
    audiences: List[str]


# TODO: Union type for multiple security definition mappings
# type SecurityDefinition = JwtSecurityDefinition;

SecurityDefinition = JwtSecurityDefinition


class ApiOptions:
    """Represents options when creating an API, such as middleware to be applied to all HTTP request to the API."""

    path: str
    middleware: Union[HttpMiddleware, List[HttpMiddleware], None]
    security_definitions: Union[dict[str, SecurityDefinition], None]
    security: Union[dict[str, List[str]], None]

    def __init__(
        self,
        path: str = "",
        middleware: List[Middleware] = None,
        security_definitions: dict[str, SecurityDefinition] = None,
        security: dict[str, List[str]] = None,
    ):
        """Construct a new API options object."""
        self.middleware = middleware
        self.security_definitions = security_definitions
        self.security = security
        self.path = path


class RouteOptions:
    """Represents options when creating a route, such as middleware to be applied to all HTTP Methods for the route."""

    middleware: Union[None, List[Middleware]]

    def __init__(self, middleware: List[Middleware] = None):
        """Construct a new route options object."""
        self.middleware = middleware


def _to_resource(b: Api) -> Resource:
    return Resource(name=b.name, type=ResourceType.Api)


def security_definition_to_grpc_declaration(security_definitions: SecurityDefinition) -> ApiSecurityDefinition:
    if security_definitions is None or len(security_definitions) == 0:
        return None
    return {
        k: ApiSecurityDefinition(
            jwt=ApiSecurityDefinitionJwt(issuer=v.issuer, audiences=v.audiences)
        ) for k, v in security_definitions.items()
    }


def security_to_grpc_declaration(security: dict[str, List[str]]) -> dict[str, ApiScopes]:
    if security is None or len(security) == 0:
        return None
    return {
        k: ApiScopes(v) for k, v in security.items()
    }


class Api(BaseResource):
    """An HTTP API."""

    app: Nitric
    name: str
    path: str
    middleware: List[HttpMiddleware]
    routes: List[Route]
    security_definitions: dict[str, SecurityDefinition]
    security: dict[str, List[str]]

    def __init__(self, name: str, opts: ApiOptions = None):
        """Construct a new HTTP API."""
        if opts is None:
            opts = ApiOptions()

        self.name = name
        self.middleware = opts.middleware
        self.path = opts.path
        self.routes = []
        self.security_definitions = opts.security_definitions
        self.security = opts.security

        self._channel = new_default_channel()
        self._resources_stub = ResourceServiceStub(channel=self._channel)

    async def _register(self):
        try:
            await self._resources_stub.declare(
                resource=_to_resource(self), 
                api=ApiResource(
                    security_definitions=security_definition_to_grpc_declaration(self.security_definitions), 
                    security=security_to_grpc_declaration(self.security)
                )
            )
        except GRPCError as grpc_err:
            raise exception_from_grpc_error(grpc_err)


    def route(self, match: str, opts: RouteOptions = None) -> Route:
        """Define an HTTP route to be handled by this API."""
        if opts is None:
            opts = RouteOptions()

        r = Route(self, match, opts)
        self.routes.append(r)
        return r

    def get(self, match: str, opts: MethodOptions = None):
        """Define an HTTP route which will respond to HTTP GET requests."""
        if opts is None:
            opts = MethodOptions()

        def decorator(function: HttpMiddleware):
            r = self.route(match)
            r.get(function, opts=opts)

        return decorator

    def post(self, match: str, opts: MethodOptions = None):
        """Define an HTTP route which will respond to HTTP POST requests."""
        if opts is None:
            opts = MethodOptions()

        def decorator(function: HttpMiddleware):
            r = self.route(match)
            r.post(function, opts=opts)

        return decorator

    def delete(self, match: str, opts: MethodOptions = None):
        """Define an HTTP route which will respond to HTTP DELETE requests."""
        if opts is None:
            opts = MethodOptions()

        def decorator(function: HttpMiddleware):
            r = self.route(match)
            r.delete(function, opts=opts)

        return decorator

    def options(self, match: str, opts: MethodOptions = None):
        """Define an HTTP route which will respond to HTTP OPTIONS requests."""
        if opts is None:
            opts = MethodOptions()

        def decorator(function: HttpMiddleware):
            r = self.route(match)
            r.options(function, opts=opts)

        return decorator

    def patch(self, match: str, opts: MethodOptions = None):
        """Define an HTTP route which will respond to HTTP PATCH requests."""
        if opts is None:
            opts = MethodOptions()

        def decorator(function: HttpMiddleware):
            r = self.route(match)
            r.patch(function, opts=opts)

        return decorator


class Route:
    """An HTTP route."""

    api: Api
    path: str
    middleware: List[Middleware]

    def __init__(self, api: Api, path: str, opts: RouteOptions):
        """Define a route to be handled by the provided API."""
        self.api = api
        self.path = path
        self.middleware = opts.middleware

    def method(self, methods: List[HttpMethod], *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for multiple HTTP Methods."""
        return Method(self, methods, *middleware, opts=opts).start()

    def get(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP GET requests."""
        return self.method([HttpMethod.GET], *middleware, opts=opts)

    def post(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP POST requests."""
        return self.method([HttpMethod.POST], *middleware, opts=opts)

    def put(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP PUT requests."""
        return self.method([HttpMethod.PUT], *middleware, opts=opts)

    def patch(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP PATCH requests."""
        return self.method([HttpMethod.PATCH], *middleware, opts=opts)

    def delete(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP DELETE requests."""
        return self.method([HttpMethod.DELETE], *middleware, opts=opts)

    def options(self, *middleware: HttpMiddleware, opts: MethodOptions = None):
        """Register middleware for HTTP OPTIONS requests."""
        return self.method([HttpMethod.OPTIONS], *middleware, opts=opts)


class Method:
    """A method handler."""

    server: FunctionServer
    route: Route
    methods: List[HttpMethod]
    opts: MethodOptions

    def __init__(
        self, route: Route, methods: List[HttpMethod], *middleware: HttpMiddleware, opts: MethodOptions = None
    ):
        """Construct a method handler for the specified route."""
        self.route = route
        self.methods = methods
        self.server = FunctionServer(ApiWorkerOptions(route.api.name, route.path, methods, opts))
        self.server.http(*middleware)

    def start(self):
        """Start the server which will respond to incoming requests."""
        Nitric._register_worker(self.server)

def api(name: str) -> Api:
    """

    """
    return Nitric._create_resource(Api, name)