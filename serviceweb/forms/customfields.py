from wtforms import fields, widgets
from wtforms.widgets.core import html_params, HTMLString


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


_BUTTON = """\

<a href="%s" class="editLink btn btn-default btn-xs" type="button">
  <span class="glyphicon glyphicon-%s" aria-hidden="true"></span>
  %s
</a>"""


class ExtendableListWidget(widgets.ListWidget):

    def _get_button(self, label="", target='#', icon="pencil"):
        return _BUTTON % (target, icon, label)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]

        for subfield in field:
            html.append('<li>')
            if self.prefix_label:
                html.append('%s %s' % (subfield.label, subfield()))
            else:
                html.append('%s %s' % (subfield(), subfield.label))

            table, entry_id = field.table, subfield.data
            target = '/%s/%s/edit?inline=1' % (table, entry_id)
            html.append(self._get_button('', target))
            html.append('</li>')

        html.append('</%s>' % self.html_tag)
        target = 'add_relation/%s?inline=1' % field.table
        html.append(self._get_button('Add', target, 'plus'))
        return HTMLString(''.join(html))


class JsonListField(fields.SelectMultipleField):
    widget = ExtendableListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

    def __init__(self, *args, **kw):
        checkbox_label = kw.pop('checkbox_label', 'name')
        table = kw.pop('table', None)
        super(JsonListField, self).__init__(*args, **kw)
        if table is None:
            table = self.id.rstrip('s')
        self.cb_label = checkbox_label
        self.table = table

    def process_data(self, data):
        if data is None:
            self.data = []
        else:
            self.data = data

    def iter_choices(self):
        for entry in self.data:
            if callable(self.cb_label):
                label = self.cb_label(self, entry)
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
