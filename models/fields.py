# -*- coding: utf-8 -*-
from __future__ import absolute_import

import decimal
from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

class FixedPointField(models.Field):
    """
    Fixed-point field
    Stored as integer in the database, represented as Decimal in Python
    """

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': _("'%(value)s' value must be a decimal number."),
    }
    description = _("Fixed-point number")

    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, decimal_places=2, **kwargs):
        self.decimal_places = decimal_places
        super(FixedPointField, self).__init__(self, verbose_name, name, **kwargs)

    def to_python(self, value):
        if value is None or isinstance(value, decimal.Decimal):
            return value
        try:
            if isinstance(value, int):
                return decimal.Decimal(value) / (10 ** self.decimal_places)
            else:
                return decimal.Decimal(value)
        except decimal.InvalidOperation:
            raise exceptions.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
                params={'value': value},
            )

    def get_prep_value(self, value):
        return int(value * (10 ** self.decimal_places))
