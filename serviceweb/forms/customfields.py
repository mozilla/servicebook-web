from wtforms import fields, widgets


__all__ = ['DynamicSelectField', 'JsonListField', 'LargeTextAreaField']


class DynamicSelectField(fields.SelectField):
    def iter_choices(self):
        choices = callable(self.choices) and self.choices() or self.choice
        for value, label in choices:
            yield (value, label, self.coerce(value) == self.data)

    def pre_validate(self, form):
        choices = callable(self.choices) and self.choices() or self.choice
        for v, _ in choices:
            if self.data == v:
                break
        else:
            raise ValueError(self.gettext('Not a valid choice'))


class ExtendableListWidget(widgets.ListWidget):
    def __call__(self, field, **kwargs):
        html = super(ExtendableListWidget, self).__call__(field, **kwargs)
        bt = '<a class="btn btn-default" href="#" role="button">Add</a>'
        html += bt
        return html


class JsonListField(fields.SelectMultipleField):
    widget = ExtendableListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def __init__(self, *args, **kw):
        checkbox_label = kw.pop('checkbox_label', 'name')
        super(JsonListField, self).__init__(*args, **kw)
        self.cb_label = checkbox_label

    def process_data(self, data):
        if data is None:
            self.data = []
        else:
            self.data = data

    def iter_choices(self):
        for entry in self.data:
            if callable(self.cb_label):
                label = self.cb_label(entry)
            else:
                label = entry[self.cb_label]

            yield entry['id'], label, True

    def __call__(self, **kwargs):
        kwargs['class_'] = 'checkbox'
        return super(JsonListField, self).__call__(**kwargs)

    def pre_validate(self, form):
        # that's where we shoud convert
        self.data = [{'id': entry} for entry in self.data]


class LargeTextAreaField(fields.TextAreaField):
    def __call__(self, **kwargs):
        kwargs['rows'] = '10'
        return super(LargeTextAreaField, self).__call__(**kwargs)
