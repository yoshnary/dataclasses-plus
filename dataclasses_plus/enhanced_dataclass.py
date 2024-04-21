import dataclasses


def dataclass(cls=None, /, **kwargs):
    def wrap(cls):

        def set_attrs(attrs):
            for attr_name, attr_obj in attrs.items():
                if hasattr(cls, attr_name):
                    raise Exception(f"{cls} already has {attr_name}")
                setattr(cls, attr_name, attr_obj)

        # load primitive feature
        from dataclasses_plus.features.primitive import get_primitive_feature_attrs

        set_attrs(get_primitive_feature_attrs())

        # load json feature
        from dataclasses_plus.features.json import get_json_feature_attrs

        set_attrs(get_json_feature_attrs())

        # load yaml feature
        try:
            from dataclasses_plus.features.yaml import get_yaml_feature_attrs

            set_attrs(get_yaml_feature_attrs())
        except ImportError:
            pass

        return dataclasses.dataclass(**kwargs)(cls)

    if cls is None:
        return wrap
    else:
        return wrap(cls)
