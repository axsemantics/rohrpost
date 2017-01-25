import json

import pytest

from rohrpost.mixins import NotifyOnChange


class ReplyChannel:
    def __init__(self):
        self.data = []
        self.closed = False

    def send(self, message_dict):
        if not self.closed:
            self.data.append(json.loads(message_dict.get('text')))
            self.closed = message_dict.get('close', False)


class Message:
    def __init__(self):
        self.reply_channel = ReplyChannel()


@pytest.fixture
def message():
    return Message()


class MockModel:
    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = 1
        return self

    def delete(self, *args, **kwargs):
        pass


class PlainExampleModel(NotifyOnChange, MockModel):
    def __init__(self):
        self.pk = None
        self.name = 'test object name'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)


class ExampleSerializer:
    def __init__(self, obj):
        self.obj = obj

    @property
    def data(self):
        return {
            'serialized_id': self.obj.pk,
            'serialized_name': self.obj.name,
        }


class ModelWithAttrMixin:
    group_name = 'attribute-example-{pk}'


class ModelWithMethodMixin:
    def get_group_name(self):
        return 'method-example-{self.pk}'.format(self=self)


class ModelWithDataMixin:
    def get_push_notification_data(self, updated_fields=None):
        return {
            'extra_name': self.name,
            'extra_name_backwards': self.name[::-1],
        }


class ModelWithSerializerMixin:
    serializer_class = ExampleSerializer


@pytest.fixture
def plain_obj():
    return PlainExampleModel()


@pytest.fixture
def obj_with_attr():
    class ModelWithAttr(ModelWithAttrMixin, PlainExampleModel):
        pass
    return ModelWithAttr()


@pytest.fixture
def obj_with_method():
    class ModelWithMethod(ModelWithMethodMixin, PlainExampleModel):
        pass
    return ModelWithMethod()


@pytest.fixture
def obj_with_method_and_attr():
    class ModelWithMethodAndAttr(ModelWithMethodMixin, ModelWithAttrMixin, PlainExampleModel):
        pass
    return ModelWithMethodAndAttr()


@pytest.fixture
def obj_with_serializer():
    class ModelWithSerializer(ModelWithSerializerMixin, PlainExampleModel):
        pass
    return ModelWithSerializer()


@pytest.fixture
def obj_with_data():
    class ModelWithData(ModelWithDataMixin, PlainExampleModel):
        pass
    return ModelWithData()


@pytest.fixture
def obj_with_serializer_and_data():
    class ModelWithSerializerAndData(ModelWithSerializerMixin, ModelWithDataMixin, PlainExampleModel):
        pass
    return ModelWithSerializerAndData()
