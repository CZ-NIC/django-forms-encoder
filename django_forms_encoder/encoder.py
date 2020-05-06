"""Django forms encoder."""
from enum import Enum, unique
from typing import Any, Dict

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import Form, widgets


@unique
class WidgetType(str, Enum):
    """Widget type enum."""

    INPUT = 'input'
    TEXTAREA = 'textarea'


class DjangoFormsEncoder(DjangoJSONEncoder):
    """Django forms encoder."""

    def default(self, obj):
        """Encode django form."""
        if isinstance(obj, Form):
            return form_to_dict(obj)

        return super().default(obj)


def form_to_dict(obj):
    """Convert django form to simple dictionary."""
    form: Dict[str, Any] = {
        'fields': [],
    }
    if obj.non_field_errors():
        form['form_errors'] = obj.non_field_errors()

    for name, field in obj.fields.items():
        field_obj = {
            'name': name,
            'label': field.label or name,
            'required': field.required,
        }

        if field.help_text:
            field_obj['help_text'] = field.help_text

        if obj.errors.get(name):
            field_obj['errors'] = obj.errors.get(name)

        if obj.is_bound and obj.cleaned_data.get(name) is not None:
            field_obj['value'] = obj.cleaned_data.get(name)

        if isinstance(field.widget, widgets.Input):
            field_obj['widget'] = {
                'name': WidgetType.INPUT,
                'type': field.widget.input_type,
            }
        elif isinstance(field.widget, widgets.Textarea):
            field_obj['widget'] = {
                'name': WidgetType.TEXTAREA,
            }
        else:
            raise TypeError('Widget of type {} is not JSON serializable'.format(type(field.widget)))

        form['fields'].append(field_obj)
    return form
