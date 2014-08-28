import importlib
from rest_framework.relations import RelatedField


def nested_getattr(obj, attr):
    return reduce(getattr, attr.split("."), obj)


def get_data(obj, serializers_module=None):
    '''
    This func relies purely on convention.
    It expects that the object name has serilizer named
    <object>Serializer and that it lives in the serializer
    module of that app
    '''
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
            attr = field.source if field.source else field_name
            value = nested_getattr(obj, attr)
        data[field_name] = value

    return data
