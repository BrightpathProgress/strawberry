from typing import Any

import strawberry
from strawberry.extensions.field_extension import FieldExtension
from strawberry.types.field import StrawberryField


def test_field_extensions_applied_once():
    class ExampleFieldExtension(FieldExtension):
        applied = 0

        def apply(self, field: StrawberryField):
            self.__class__.applied += 1

        def resolve(self, next_, source, info, **kwargs: Any):
            return next_(source, info, **kwargs)

    @strawberry.type
    class Query:
        field: str = strawberry.field(extensions=[ExampleFieldExtension()])

    _public_schema = strawberry.Schema(query=Query)
    _private_schema = strawberry.Schema(query=Query)

    assert ExampleFieldExtension.applied == 1


def test_relay_node():
    @strawberry.type
    class ExampleType:
        name: str

    @strawberry.type
    class Query:
        example: ExampleType = strawberry.relay.node()

    _public_schema = strawberry.Schema(query=Query)
    _private_schema = strawberry.Schema(query=Query)
