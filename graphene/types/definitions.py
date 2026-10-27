from enum import Enum as PyEnum

from graphql import (
    GraphQLEnumType,
    GraphQLInputObjectType,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType,
)


class GrapheneGraphQLType:
    """
    A class for extending the base GraphQLType with the related
    graphene_type
    """

    def __init__(self, *args, **kwargs):
        self.graphene_type = kwargs.pop("graphene_type")
        super(GrapheneGraphQLType, self).__init__(*args, **kwargs)

    def __copy__(self):
        result = GrapheneGraphQLType(graphene_type=self.graphene_type)
        result.__dict__.update(self.__dict__)
        return result


class GrapheneInterfaceType(GrapheneGraphQLType, GraphQLInterfaceType):
    pass


class GrapheneUnionType(GrapheneGraphQLType, GraphQLUnionType):
    pass


class GrapheneObjectType(GrapheneGraphQLType, GraphQLObjectType):
    pass


class GrapheneScalarType(GrapheneGraphQLType, GraphQLScalarType):
    pass


class GrapheneEnumType(GrapheneGraphQLType, GraphQLEnumType):
    def get_enum_member(self, value):
        """
        Return the Python enum member for an enum member, value or name.

        A hashable value that matches nothing is returned unchanged, so GraphQLEnumType raises its usual
        "cannot represent value" error for it, on graphql-core 3.2 and 3.3 alike.
        """
        if not isinstance(value, PyEnum):
            enum = self.graphene_type._meta.enum
            try:
                # Try and get enum by value
                value = enum(value)
            except ValueError:
                # Try and get enum by name
                try:
                    value = enum[value]
                except KeyError:
                    pass
        return value

    def serialize(self, value):
        return super(GrapheneEnumType, self).serialize(self.get_enum_member(value))

    def coerce_output_value(self, value):
        # graphql-core 3.3 calls coerce_output_value() instead of serialize() for output values.
        return super(GrapheneEnumType, self).coerce_output_value(
            self.get_enum_member(value)
        )


class GrapheneInputObjectType(GrapheneGraphQLType, GraphQLInputObjectType):
    pass
