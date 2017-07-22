from django import template
from django import forms

register = template.Library()


@register.filter(name="bootstrap_form_control")
def form_control(form_input: forms.BoundField):
    """Add the form control class to an input."""

    form_input.field.widget.attrs["class"] = "form-control"
    return form_input
