import json
from collections import defaultdict

LOGGED_DATA = defaultdict(list)


def mocked_send_to_group(*, group_name, message):
    LOGGED_DATA[group_name].append(json.loads(message))


def mocked_transaction_commit(func):
    func()


def test_without_name(plain_obj, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    plain_obj.save()
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 1
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "create"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1

    # update
    plain_obj.save()
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 2
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1

    # delete
    plain_obj.delete()
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 3
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "delete"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1
    LOGGED_DATA["plainexamplemodel-1"] = []


def test_send_update_fields(plain_obj, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    plain_obj.save()
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 1
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "create"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1
    assert (
        "updated_fields" not in LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]
    )

    # update without fields
    plain_obj.save(update_fields=[])
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 2
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1
    assert (
        "updated_fields" not in LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]
    )

    # update with fields
    plain_obj.save(update_fields=["something", "something_else"])
    assert len(LOGGED_DATA["plainexamplemodel-1"]) == 3
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["id"] == 1
    assert (
        "something_else"
        in LOGGED_DATA["plainexamplemodel-1"][-1]["data"]["object"]["updated_fields"]
    )


def test_with_attribute_name(obj_with_attr, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_attr.save()
    assert len(LOGGED_DATA["attribute-example-1"]) == 1
    assert LOGGED_DATA["attribute-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["type"] == "create"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["object"]["id"] == 1

    # update
    obj_with_attr.save()
    assert len(LOGGED_DATA["attribute-example-1"]) == 2
    assert LOGGED_DATA["attribute-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["object"]["id"] == 1

    # delete
    obj_with_attr.delete()
    assert len(LOGGED_DATA["attribute-example-1"]) == 3
    assert LOGGED_DATA["attribute-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["type"] == "delete"
    assert LOGGED_DATA["attribute-example-1"][-1]["data"]["object"]["id"] == 1
    LOGGED_DATA["attribute-example-1"] = []


def test_with_method_name(obj_with_method, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_method.save()
    assert len(LOGGED_DATA["method-example-1"]) == 1
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "create"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1

    # update
    obj_with_method.save()
    assert len(LOGGED_DATA["method-example-1"]) == 2
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1

    # delete
    obj_with_method.delete()
    assert len(LOGGED_DATA["method-example-1"]) == 3
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "delete"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1
    LOGGED_DATA["method-example-1"] = []


def test_with_method_and_attr(obj_with_method_and_attr, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_method_and_attr.save()
    assert len(LOGGED_DATA["method-example-1"]) == 1
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "create"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1

    # update
    obj_with_method_and_attr.save()
    assert len(LOGGED_DATA["method-example-1"]) == 2
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1

    # delete
    obj_with_method_and_attr.delete()
    assert len(LOGGED_DATA["method-example-1"]) == 3
    assert LOGGED_DATA["method-example-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["type"] == "delete"
    assert LOGGED_DATA["method-example-1"][-1]["data"]["object"]["id"] == 1
    LOGGED_DATA["method-example-1"] = []


def test_with_additional_data(obj_with_data, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_data.save()
    assert len(LOGGED_DATA["modelwithdata-1"]) == 1
    assert LOGGED_DATA["modelwithdata-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithdata-1"][-1]["data"]["type"] == "create"
    assert (
        LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]

    # update
    obj_with_data.save()
    assert len(LOGGED_DATA["modelwithdata-1"]) == 2
    assert LOGGED_DATA["modelwithdata-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithdata-1"][-1]["data"]["type"] == "update"
    assert (
        LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]

    # delete
    obj_with_data.delete()
    assert len(LOGGED_DATA["modelwithdata-1"]) == 3
    assert LOGGED_DATA["modelwithdata-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithdata-1"][-1]["data"]["type"] == "delete"
    assert (
        LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithdata-1"][-1]["data"]["object"]
    LOGGED_DATA["modelwithdata-1"] = []


def test_with_serializer(obj_with_serializer, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_serializer.save()
    assert len(LOGGED_DATA["modelwithserializer-1"]) == 1
    assert LOGGED_DATA["modelwithserializer-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithserializer-1"][-1]["data"]["type"] == "create"
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_id"] == 1
    )
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]

    # update
    obj_with_serializer.save()
    assert len(LOGGED_DATA["modelwithserializer-1"]) == 2
    assert LOGGED_DATA["modelwithserializer-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithserializer-1"][-1]["data"]["type"] == "update"
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_id"] == 1
    )
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]

    # delete
    obj_with_serializer.delete()
    assert len(LOGGED_DATA["modelwithserializer-1"]) == 3
    assert LOGGED_DATA["modelwithserializer-1"][-1]["type"] == "subscription-update"
    assert LOGGED_DATA["modelwithserializer-1"][-1]["data"]["type"] == "delete"
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_id"] == 1
    )
    assert (
        LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]["serialized_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializer-1"][-1]["data"]["object"]
    LOGGED_DATA["modelwithserializer-1"] = []


def test_with_serializer_and_data(obj_with_serializer_and_data, monkeypatch):
    monkeypatch.setattr("rohrpost.mixins.send_to_group", mocked_send_to_group)
    monkeypatch.setattr(
        "rohrpost.mixins.on_transaction_commit", mocked_transaction_commit
    )

    # create
    obj_with_serializer_and_data.save()
    assert len(LOGGED_DATA["modelwithserializeranddata-1"]) == 1
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["type"] == "subscription-update"
    )
    assert LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["type"] == "create"
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    assert (
        "serialized_id"
        not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    )

    # update
    obj_with_serializer_and_data.save()
    assert len(LOGGED_DATA["modelwithserializeranddata-1"]) == 2
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["type"] == "subscription-update"
    )
    assert LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["type"] == "update"
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    assert (
        "serialized_id"
        not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    )

    # delete
    obj_with_serializer_and_data.delete()
    assert len(LOGGED_DATA["modelwithserializeranddata-1"]) == 3
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["type"] == "subscription-update"
    )
    assert LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["type"] == "delete"
    assert (
        LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]["extra_name"]
        == "test object name"
    )
    assert "id" not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    assert (
        "serialized_id"
        not in LOGGED_DATA["modelwithserializeranddata-1"][-1]["data"]["object"]
    )
    LOGGED_DATA["modelwithserializeranddata-1"] = []
