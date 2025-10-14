class MetaLocator(type):

    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if isinstance(value, str):
                if value.startswith("//") or value.startswith(".//") or value.startswith("(//"):
                    attrs[key] = ("xpath", value)
                elif value.startswith(".") or value.startswith("#"):
                    attrs[key] = ("css selector", value)
        return type.__new__(cls, name, bases, attrs)
