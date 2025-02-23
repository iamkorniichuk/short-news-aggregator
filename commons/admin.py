from django.utils.safestring import mark_safe


class ExternalLinkTag:
    """
    On `href`, `alt`, `inner_text` will be called `getattr()`.

    To avoid this behaviour pass them using `**extra_attributes`.
    """

    def __init__(self, href, alt, inner_text, open_new_tab=False, **extra_attributes):
        self.href = href
        self.alt = alt
        self.inner_text = inner_text
        if open_new_tab:
            extra_attributes["target"] = "_blank"
            extra_attributes["rel"] = "noopener noreferrer"
        self.extra_attributes = extra_attributes

    def render(self, obj):
        return self(obj)

    def __call__(self, obj):
        inner_text = self.extra_attributes.pop("inner_text", None)
        if not inner_text:
            inner_text = self.get_model_value(obj, self.inner_text)

        main_attributes = {
            "href": self.get_model_value(obj, self.href),
            "alt": self.get_model_value(obj, self.alt),
        }

        main_attributes.update(self.extra_attributes)
        attributes = self.render_attributes(**main_attributes)

        return mark_safe(f"<a {attributes}>{inner_text}</a>")

    @classmethod
    def get_model_value(self, model, attribute_name):
        value = getattr(model, attribute_name)
        if callable(value):
            value = value()
        return value

    @classmethod
    def render_attributes(cls, **attributes):
        results = []
        for name, value in attributes.items():
            results.append(f'{name}="{value}"')
        return " ".join(results)
