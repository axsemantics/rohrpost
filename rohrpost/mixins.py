import json

from .message import build_message

try:
    from channels import Group
except:
    Group = None
    print('Channels is not installed, running in test mode!')


class PushNotificationOnChangeModelMixin:
    """
    This model mixin class sends rohrpost messages every time an object is created, updated, or
    deleted, to the corresponding group. The group is named, most important first:
        - As the result of get_group_name() if the object has such a method
        - As the result of group_name.format(pk=object.pk) if the object/class has a group_name
          attribute
        - As the result of '{class_name}-{pk}'.format(class_name=object.__class__.__name__.lower()
          pk=object.pk) otherwise
    The serialized object will be taken either from:
        - The result of get_push_notification_data() if such a method exists, else
        - The result of serializer_class(self).data, if such an attribute exists, else
        - {"id": self.pk}
    The serialized object will also contain an 'updated_fields' attribute with a list *if*
    'updated_fields' was not set by the get_push_notification_data() or the serializer_class
    *and* if it was set when calling the save() method.

    The message will look like this:
    {
        "id": <some id>,
        "type": "subscription-update",
        "data": {
            "type": <create|update|delete>,
            "group": <group-name>,
            "object": <serialized object>,
        }
    }
    """
    def _get_group_name(self):
        if hasattr(self, "get_group_name"):
            return self.get_group_name()
        if hasattr(self, "group_name"):
            return self.group_name.format(pk=self.pk)
        return '{class_name}-{pk}'.format(
            class_name=self.__class__.__name__.lower(),
            pk=self.pk,
        )

    def _get_push_data(self):
        if hasattr(self, 'get_push_notification_data'):
            obj_data = self.get_push_notification_data()
        elif hasattr(self, 'serializer_class'):
            obj_data = self.serializer_class(self).data
        else:
            obj_data = {'id': self.pk}
        return obj_data

    def _send_notify(self, message_type, updated_fields=None):
        group_name = self._get_group_name()
        message_data = {
            'group': self._get_group_name(),
            'type': message_type,
            'object': self._get_push_data(),
        }
        if updated_fields and 'updated_fields' not in message_data['object']:
            message_data['object']['updated_fields'] = updated_fields

        Group(group_name).send({
            'text': json.dumps(build_message(
                generate_id=True,
                handler='subscription-update',
                **message_data,
            ))
        })

    def save(self, *args, **kwargs):
        message_type = 'update' if self.pk else 'create'
        ret = super().save(*args, **kwargs)
        self._send_notify(message_type, updated_fields=kwargs.get('update_fields'))
        return ret

    def delete(self, *args, **kwargs):
        self._send_notify('delete')
        return super().delete(*args, **kwargs)
