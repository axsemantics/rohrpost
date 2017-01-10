import json
from collections import defaultdict

LOGGED_DATA = defaultdict(list)


class MockGroup:
    def __init__(self, name):
        self.name = name

    def send(self, message_dict):
        global LOGGED_DATA
        LOGGED_DATA[self.name].append(json.loads(message_dict['text']))


def test_without_name(plain_obj, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    plain_obj.save()
    assert len(LOGGED_DATA['plainexamplemodel-1']) == 1
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['object']['id'] == 1

    # update
    plain_obj.save()
    assert len(LOGGED_DATA['plainexamplemodel-1']) == 2
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['object']['id'] == 1

    # delete
    plain_obj.delete()
    assert len(LOGGED_DATA['plainexamplemodel-1']) == 3
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['plainexamplemodel-1'][-1]['data']['object']['id'] == 1
    LOGGED_DATA['plainexamplemodel-1'] = []


def test_with_attribute_name(obj_with_attr, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_attr.save()
    assert len(LOGGED_DATA['attribute-example-1']) == 1
    assert LOGGED_DATA['attribute-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['object']['id'] == 1

    # update
    obj_with_attr.save()
    assert len(LOGGED_DATA['attribute-example-1']) == 2
    assert LOGGED_DATA['attribute-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['object']['id'] == 1

    # delete
    obj_with_attr.delete()
    assert len(LOGGED_DATA['attribute-example-1']) == 3
    assert LOGGED_DATA['attribute-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['attribute-example-1'][-1]['data']['object']['id'] == 1
    LOGGED_DATA['attribute-example-1'] = []


def test_with_method_name(obj_with_method, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_method.save()
    assert len(LOGGED_DATA['method-example-1']) == 1
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1

    # update
    obj_with_method.save()
    assert len(LOGGED_DATA['method-example-1']) == 2
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1

    # delete
    obj_with_method.delete()
    assert len(LOGGED_DATA['method-example-1']) == 3
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1
    LOGGED_DATA['method-example-1'] = []


def test_with_method_and_attr(obj_with_method_and_attr, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_method_and_attr.save()
    assert len(LOGGED_DATA['method-example-1']) == 1
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1

    # update
    obj_with_method_and_attr.save()
    assert len(LOGGED_DATA['method-example-1']) == 2
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1

    # delete
    obj_with_method_and_attr.delete()
    assert len(LOGGED_DATA['method-example-1']) == 3
    assert LOGGED_DATA['method-example-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['method-example-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['method-example-1'][-1]['data']['object']['id'] == 1
    LOGGED_DATA['method-example-1'] = []


def test_with_additional_data(obj_with_data, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_data.save()
    assert len(LOGGED_DATA['modelwithdata-1']) == 1
    assert LOGGED_DATA['modelwithdata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['extra_name'] == 'test object name'

    # update
    obj_with_data.save()
    assert len(LOGGED_DATA['modelwithdata-1']) == 2
    assert LOGGED_DATA['modelwithdata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['extra_name'] == 'test object name'

    # delete
    obj_with_data.delete()
    assert len(LOGGED_DATA['modelwithdata-1']) == 3
    assert LOGGED_DATA['modelwithdata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithdata-1'][-1]['data']['object']['extra_name'] == 'test object name'
    LOGGED_DATA['modelwithdata-1'] = []


def test_with_serializer(obj_with_serializer, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_serializer.save()
    print(LOGGED_DATA)
    assert len(LOGGED_DATA['modelwithserializer-1']) == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_name'] == 'test object name'

    # update
    obj_with_serializer.save()
    assert len(LOGGED_DATA['modelwithserializer-1']) == 2
    assert LOGGED_DATA['modelwithserializer-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_name'] == 'test object name'

    # delete
    obj_with_serializer.delete()
    assert len(LOGGED_DATA['modelwithserializer-1']) == 3
    assert LOGGED_DATA['modelwithserializer-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializer-1'][-1]['data']['object']['serialized_name'] == 'test object name'
    LOGGED_DATA['modelwithserializer-1'] = []


def test_with_serializer_and_data(obj_with_serializer_and_data, monkeypatch):
    monkeypatch.setattr('rohrpost.mixins.Group', MockGroup)

    # create
    obj_with_serializer_and_data.save()
    assert len(LOGGED_DATA['modelwithserializeranddata-1']) == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['type'] == 'create'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_name'] == 'test object name'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['extra_name'] == 'test object name'

    # update
    obj_with_serializer_and_data.save()
    assert len(LOGGED_DATA['modelwithserializeranddata-1']) == 2
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['type'] == 'update'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_name'] == 'test object name'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['extra_name'] == 'test object name'

    # delete
    obj_with_serializer_and_data.delete()
    assert len(LOGGED_DATA['modelwithserializeranddata-1']) == 3
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['type'] == 'subscription-update'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['type'] == 'delete'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_id'] == 1
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['serialized_name'] == 'test object name'
    assert LOGGED_DATA['modelwithserializeranddata-1'][-1]['data']['object']['extra_name'] == 'test object name'
    LOGGED_DATA['modelwithserializeranddata-1'] = []
