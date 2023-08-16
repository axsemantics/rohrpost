# pylint: disable=no-member,too-few-public-methods
import json
from typing import Optional, Sequence

from django.db.transaction import on_commit as on_transaction_commit

from .message import TolerantJSONEncoder, build_message, send_to_group


class NotifyBase:
    encoder = TolerantJSONEncoder

    def _get_group_name(self, message_type: str = "") -> str:
        if hasattr(self, "get_group_name"):
            return self.get_group_name(message_type=message_type)
        if hasattr(self, "group_name"):
            return self.group_name.format(pk=self.pk)  # type: ignore[attr-defined]
        return "{class_name}-{pk}".format(  # pylint: disable=consider-using-f-string
            class_name=self.__class__.__name__.lower(),
            pk=self.pk,  # type: ignore[attr-defined]
        )

    def _get_push_data(
        self,
        updated_fields: Optional[Sequence[str]] = None,
        message_type: Optional[str] = None,
    ) -> dict:
        if hasattr(self, "get_push_notification_data"):
            obj_data = self.get_push_notification_data(
                updated_fields=updated_fields, message_type=message_type
            )
        elif hasattr(self, "serializer_class"):
            obj_data = self.serializer_class(self).data
        else:
            obj_data = {"id": self.pk}  # type: ignore[attr-defined]
        return obj_data

    def _get_message_type(self, message_type: str) -> str:
        return message_type

    def _send_notify(
        self,
        message_type: str,
        updated_fields: Optional[Sequence[str]] = None,
        data: Optional[dict] = None,
        always_send: bool = True,
    ) -> None:
        group_name = self._get_group_name(message_type=message_type)

        message_object = data or self._get_push_data(
            updated_fields=updated_fields, message_type=message_type
        )

        if updated_fields and "updated_fields" not in message_object:
            message_object["updated_fields"] = updated_fields

        if message_type == "update" and updated_fields and always_send is False:
            if not set(updated_fields) & set(message_object.keys()):
                return

        message_data = {
            "group": group_name,
            "type": self._get_message_type(message_type),
            "object": message_object,
        }

        payload = json.dumps(
            build_message(
                generate_id=True, handler="subscription-update", data=message_data
            ),
            cls=self.encoder,
        )

        on_transaction_commit(
            lambda: send_to_group(group_name=group_name, message=payload)
        )


class NotifyOnCreate(NotifyBase):
    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        initial_pk = self.pk  # type: ignore[attr-defined]
        ret = super().save(*args, **kwargs)  # type: ignore[misc]
        if not initial_pk:
            self._send_notify("create", updated_fields=kwargs.get("update_fields"))
        return ret


class NotifyOnUpdate(NotifyBase):
    rohrpost_always_send = (
        True  # Toggle if even data not reflecting update_fields should be sent
    )

    def save(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        initial_pk = self.pk  # type: ignore[attr-defined]
        ret = super().save(*args, **kwargs)  # type: ignore[misc]
        if initial_pk:
            self._send_notify(
                "update",
                updated_fields=kwargs.get("update_fields"),
                always_send=self.rohrpost_always_send,
            )
        return ret


class NotifyOnDelete(NotifyBase):
    def delete(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        self._send_notify("delete")
        return super().delete(*args, **kwargs)  # type: ignore[misc]


class NotifyOnChange(NotifyOnCreate, NotifyOnUpdate, NotifyOnDelete):
    """
    This model mixin class sends rohrpost messages every time an object is created, updated, or
    deleted, to the corresponding group. The group is named, most important first:
        - As the result of get_group_name() if the object has such a method
        - As the result of group_name.format(pk=object.pk) if the object/class has a group_name
          attribute
        - As the result of '{class_name}-{pk}'.format(class_name=object.__class__.__name__.lower()
          pk=object.pk) otherwise
    The serialized object will be taken either from:
        - The result of get_push_notification_data(updated_fields=None),
          if such a method exists, else
        - The result of serializer_class(self).data, if such an attribute exists, else
        - {"id": self.pk}
    The serialized object will also contain an 'updated_fields' attribute with a list *if*
    'updated_fields' was not set by the get_push_notification_data() or the serializer_class
    *and* if it was set when calling the save() method.
    get_push_notification_data() receives a list of updated_fields.

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
