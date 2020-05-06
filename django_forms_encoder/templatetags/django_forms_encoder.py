"""Encoder template tags."""
from django import template

from django_forms_encoder.encoder import form_to_dict

register = template.Library()


register.filter('encode_form', form_to_dict)
