"""Task."""
import enum
from typing import Any

import marshmallow
from marshmallow import Schema
from marshmallow_enum import EnumField  # type: ignore

# from SpiffWorkflow.camunda.specs.UserTask import Form  # type: ignore


class MultiInstanceType(enum.Enum):
    """MultiInstanceType."""

    none = "none"
    looping = "looping"
    parallel = "parallel"
    sequential = "sequential"


class Task:
    """Task."""

    ##########################################################################
    #    Custom properties and validations defined in Camunda form fields    #
    ##########################################################################

    # Custom task title
    PROP_EXTENSIONS_TITLE = "display_name"
    PROP_EXTENSIONS_CLEAR_DATA = "clear_data"

    # Field Types
    FIELD_TYPE_STRING = "string"
    FIELD_TYPE_LONG = "long"
    FIELD_TYPE_BOOLEAN = "boolean"
    FIELD_TYPE_DATE = "date"
    FIELD_TYPE_ENUM = "enum"
    FIELD_TYPE_TEXTAREA = "textarea"  # textarea: Multiple lines of text
    FIELD_TYPE_AUTO_COMPLETE = "autocomplete"
    FIELD_TYPE_FILE = "file"
    FIELD_TYPE_FILES = "files"  # files: Multiple files
    FIELD_TYPE_TEL = "tel"  # tel: Phone number
    FIELD_TYPE_EMAIL = "email"  # email: Email address
    FIELD_TYPE_URL = "url"  # url: Website address

    FIELD_PROP_AUTO_COMPLETE_MAX = (
        "autocomplete_num"  # Not used directly, passed in from the front end.
    )

    # Required field
    FIELD_CONSTRAINT_REQUIRED = "required"

    # Field properties and expressions Expressions
    FIELD_PROP_REPEAT = "repeat"
    FIELD_PROP_READ_ONLY = "read_only"
    FIELD_PROP_LDAP_LOOKUP = "ldap.lookup"
    FIELD_PROP_READ_ONLY_EXPRESSION = "read_only_expression"
    FIELD_PROP_HIDE_EXPRESSION = "hide_expression"
    FIELD_PROP_REQUIRED_EXPRESSION = "required_expression"
    FIELD_PROP_LABEL_EXPRESSION = "label_expression"
    FIELD_PROP_REPEAT_HIDE_EXPRESSION = "repeat_hide_expression"
    FIELD_PROP_VALUE_EXPRESSION = "value_expression"

    # Enum field options
    FIELD_PROP_SPREADSHEET_NAME = "spreadsheet.name"
    FIELD_PROP_DATA_NAME = "data.name"
    FIELD_PROP_VALUE_COLUMN = "value.column"
    FIELD_PROP_LABEL_COLUMN = "label.column"

    # Enum field options values pulled from task data

    # Group and Repeat functions
    FIELD_PROP_GROUP = "group"
    FIELD_PROP_REPLEAT = "repeat"
    FIELD_PROP_REPLEAT_TITLE = "repeat_title"
    FIELD_PROP_REPLEAT_BUTTON = "repeat_button_label"

    # File specific field properties
    FIELD_PROP_DOC_CODE = "doc_code"  # to associate a file upload field with a doc code
    FIELD_PROP_FILE_DATA = (
        "file_data"  # to associate a bit of data with a specific file upload file.
    )

    # Additional properties
    FIELD_PROP_ENUM_TYPE = "enum_type"
    FIELD_PROP_BOOLEAN_TYPE = "boolean_type"
    FIELD_PROP_TEXT_AREA_ROWS = "rows"
    FIELD_PROP_TEXT_AREA_COLS = "cols"
    FIELD_PROP_TEXT_AREA_AUTO = "autosize"
    FIELD_PROP_PLACEHOLDER = "placeholder"
    FIELD_PROP_DESCRIPTION = "description"
    FIELD_PROP_MARKDOWN_DESCRIPTION = "markdown_description"
    FIELD_PROP_HELP = "help"

    ##########################################################################

    def __init__(
        self,
        id: str,
        name: str,
        title: str,
        type: str,
        state: str,
        lane: str,
        form: None,
        documentation: str,
        data: dict[str, Any],
        multi_instance_type: MultiInstanceType,
        multi_instance_count: str,
        multi_instance_index: str,
        process_name: str,
        properties: dict,
    ):
        """__init__."""
        self.id = id
        self.name = name
        self.title = title
        self.type = type
        self.state = state
        self.form = None
        self.documentation = documentation
        self.data = data
        self.lane = lane
        self.multi_instance_type = (
            multi_instance_type  # Some tasks have a repeat behavior.
        )
        self.multi_instance_count = (
            multi_instance_count  # This is the number of times the task could repeat.
        )
        self.multi_instance_index = (
            multi_instance_index  # And the index of the currently repeating task.
        )
        self.process_name = process_name
        self.properties = properties  # Arbitrary extension properties from BPMN editor.

    @classmethod
    def valid_property_names(cls) -> list[str]:
        """Valid_property_names."""
        return [
            value for name, value in vars(cls).items() if name.startswith("FIELD_PROP")
        ]

    @classmethod
    def valid_field_types(cls) -> list[str]:
        """Valid_field_types."""
        return [
            value for name, value in vars(cls).items() if name.startswith("FIELD_TYPE")
        ]


class OptionSchema(Schema):
    """OptionSchema."""

    class Meta:
        """Meta."""

        fields = ["id", "name", "data"]


class ValidationSchema(Schema):
    """ValidationSchema."""

    class Meta:
        """Meta."""

        fields = ["name", "config"]


class FormFieldPropertySchema(Schema):
    """FormFieldPropertySchema."""

    class Meta:
        """Meta."""

        fields = ["id", "value"]


class FormFieldSchema(Schema):
    """FormFieldSchema."""

    class Meta:
        """Meta."""

        fields = [
            "id",
            "type",
            "label",
            "default_value",
            "options",
            "validation",
            "properties",
            "value",
        ]

    default_value = marshmallow.fields.String(required=False, allow_none=True)
    options = marshmallow.fields.List(marshmallow.fields.Nested(OptionSchema))
    validation = marshmallow.fields.List(marshmallow.fields.Nested(ValidationSchema))
    properties = marshmallow.fields.List(
        marshmallow.fields.Nested(FormFieldPropertySchema)
    )


# class FormSchema(Schema):
#     """FormSchema."""
#
#     key = marshmallow.fields.String(required=True, allow_none=False)
#     fields = marshmallow.fields.List(marshmallow.fields.Nested(FormFieldSchema))


class TaskSchema(Schema):
    """TaskSchema."""

    class Meta:
        """Meta."""

        fields = [
            "id",
            "name",
            "title",
            "type",
            "state",
            "lane",
            "form",
            "documentation",
            "data",
            "multi_instance_type",
            "multi_instance_count",
            "multi_instance_index",
            "process_name",
            "properties",
        ]

    multi_instance_type = EnumField(MultiInstanceType)
    documentation = marshmallow.fields.String(required=False, allow_none=True)
    # form = marshmallow.fields.Nested(FormSchema, required=False, allow_none=True)
    title = marshmallow.fields.String(required=False, allow_none=True)
    process_name = marshmallow.fields.String(required=False, allow_none=True)
    lane = marshmallow.fields.String(required=False, allow_none=True)

    @marshmallow.post_load
    def make_task(self, data: dict[str, Any], **kwargs: dict) -> Task:
        """Make_task."""
        return Task(**data)
