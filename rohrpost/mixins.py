import json

try:
    from channels import Group
except:
    Group = None
    print('Channels is not installed, running in test mode!')

from .message import build_message


class PushNotificationOnChangeModelMixin:
    """
    This model mixin class sends rohrpost messages every time an object is created, updated, or
    deleted, to the corresponding group. The group is named:
        - As the result of get_group_name() if the object has such a method
        - As the result of group_name.format(pk=object.pk) if the object/class has a group_name
          attribute
        - As the result of '{class_name}-{pk}'.format(class_name=object.__class__.__name__.lower()
          pk=object.pk) otherwise

    The message will look like this:
    {
        "id": <some id>,
        "type": "subscription-update",
        "data": {
            "type": <create|update|delete>,
            "group": <group-name>,
            "object": <serialized object if object.serializer_class is set, else
                       {"id": <object.id>}>, "id" being a guaranteed key
                      plus the output of <additional data from object.get_push_notification_data()>
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
        obj_data = {'id': self.pk}
        if hasattr(self, 'serializer_class'):
            obj_data.update(self.serializer_class(self).data)
        if hasattr(self, 'get_push_notification_data'):
            obj_data.update(self.get_push_notification_data())
        return obj_data

    def _send_notify(self, message_type):
        group_name = self._get_group_name()
        message_data = {
            'group': self._get_group_name(),
            'type': message_type,
            'object': self._get_push_data(),
        }
        Group(group_name).send({
            'text': json.dumps(build_message(
                generate_id=True,
                handler='subscription-update',
                **message_data,
            ))
        })

    def save(self, *args, **kwargs):
        message_type = 'update' if self.pk else 'create'
        ret = super().save(self, *args, **kwargs)
        self._send_notify(message_type)
        return ret

    def delete(self, *args, **kwargs):
        self._send_notify('delete')
        return super().delete(*args, **kwargs)
