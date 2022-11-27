import uuid

from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core import checks


class TokenAutorizateField(models.CharField):
    description = _("Token for registration")

    def __init__(self, auto_create_token=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_created_token = auto_create_token

    def _check_max_length_attribute(self, **kwargs):
        validations = super(TokenAutorizateField, self)._check_max_length_attribute(
            **kwargs
        )
        if validations:
            return validations

        if self.max_length < 33:
            return [
                checks.Error(
                    "CharFields 'max_length' must been only > 33",
                    obj=self,
                    id="fields.E122",
                )
            ]
        else:
            return validations

    def pre_save(self, model_instance, add):
        if self.auto_created_token and not self.get_prep_value(model_instance):
            value = uuid.uuid4().hex
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(TokenAutorizateField, self).pre_save(model_instance, add)
