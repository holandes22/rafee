import importlib
from rest_framework.relations import RelatedField


def nested_getattr(obj, attr):
    return reduce(getattr, attr.split("."), obj)


def get_data(obj, serializers_module=None):
    cls_name = obj.__class__.__name__
    if not serializers_module:
        serializers_module = importlib.import_module(
            'rafee.{}.serializers'.format(obj._meta.app_label)
        )
    serializer_cls = getattr(
        serializers_module,
        '{}Serializer'.format(cls_name),
    )
    serializer = serializer_cls(obj)
    data = {}
    for field_name in serializer.get_fields():
        field = serializer.fields[field_name]
        if isinstance(field, RelatedField):
            value = field.field_to_native(obj, field_name)
        else:
            value = nested_getattr(obj, field_name)
        data[field_name] = value

    return data
