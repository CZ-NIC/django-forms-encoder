import json
from datetime import datetime

from django import forms
from django.test import SimpleTestCase

from django_forms_encoder import DjangoFormsEncoder
from django_forms_encoder.encoder import form_to_dict


class TestDjangoFormsEncoder(SimpleTestCase):
    """Test django forms encoder."""

    def test_not_form(self):
        obj = datetime(2020, 1, 1)
        self.assertEqual(
            json.dumps(obj, cls=DjangoFormsEncoder),
            '"2020-01-01T00:00:00"'
        )

    def test_form(self):
        class TestForm(forms.Form):
            username = forms.CharField()
            password = forms.CharField()

        self.assertEqual(
            json.loads(json.dumps(TestForm(), cls=DjangoFormsEncoder)),
            form_to_dict(TestForm()),
        )


class TestFormToDict(SimpleTestCase):
    """Test form_to_dict function."""

    def test_field_name(self):
        class TestForm(forms.Form):
            username = forms.CharField()
            password = forms.CharField()

        form = form_to_dict(TestForm())
        self.assertEqual(form['fields'][0]['name'], 'username')
        self.assertEqual(form['fields'][1]['name'], 'password')

    def test_field_label(self):
        class TestForm(forms.Form):
            username = forms.CharField(label='Name of the user')
            password = forms.CharField()

        form = form_to_dict(TestForm())
        self.assertEqual(form['fields'][0]['label'], 'Name of the user')
        self.assertEqual(form['fields'][1]['label'], 'password')

    def test_field_required(self):
        class TestForm(forms.Form):
            username = forms.CharField(required=True)
            password = forms.CharField(required=False)

        form = form_to_dict(TestForm())
        self.assertEqual(form['fields'][0]['required'], True)
        self.assertEqual(form['fields'][1]['required'], False)

    def test_field_help_text(self):
        class TestForm(forms.Form):
            username = forms.CharField(help_text='Must be unique')
            password = forms.CharField()

        form = form_to_dict(TestForm())
        self.assertEqual(form['fields'][0]['help_text'], 'Must be unique')
        self.assertNotIn('help_text', form['fields'][1])

    def test_field_widget(self):
        class TestForm(forms.Form):
            username = forms.CharField()
            password = forms.CharField(widget=forms.PasswordInput)
            description = forms.CharField(widget=forms.Textarea)
            is_admin = forms.BooleanField()

        form = form_to_dict(TestForm())
        self.assertEqual(form['fields'][0]['widget'], {'name': 'input', 'type': 'text'})
        self.assertEqual(form['fields'][1]['widget'], {'name': 'input', 'type': 'password'})
        self.assertEqual(form['fields'][2]['widget'], {'name': 'textarea'})
        self.assertEqual(form['fields'][3]['widget'], {'name': 'input', 'type': 'checkbox'})

    def test_field_unknown_widget(self):
        class UnknownWidget(forms.Widget):
            pass

        class TestForm(forms.Form):
            username = forms.CharField(widget=UnknownWidget)

        with self.assertRaisesRegex(TypeError, 'Widget of type .*UnknownWidget.* is not JSON serializable'):
            form_to_dict(TestForm())

    def test_field_errors(self):
        class TestForm(forms.Form):
            username = forms.CharField(required=True)
            password = forms.CharField(required=False)
            age = forms.IntegerField(required=False)

            def clean(self):
                self.add_error('username', 'Must be a name.')
                self.add_error('password', 'Must not be empty.')

        form = form_to_dict(TestForm(data={}))
        self.assertEqual(form['fields'][0]['errors'], ['This field is required.', 'Must be a name.'])
        self.assertEqual(form['fields'][1]['errors'], ['Must not be empty.'])
        self.assertNotIn('errors', form['fields'][2])

    def test_form_errors(self):
        class TestForm(forms.Form):
            username = forms.CharField()

            def clean(self):
                self.add_error(None, 'My hovercraft is full of eels!')
                self.add_error(None, 'Keep it simple!')

        form = form_to_dict(TestForm(data={}))
        self.assertEqual(form['form_errors'], ['My hovercraft is full of eels!', 'Keep it simple!'])

    def test_field_value(self):
        class TestForm(forms.Form):
            username = forms.CharField()
            age = forms.IntegerField()

        form_obj = TestForm(data={'username': 'admin', 'age': 42})
        self.assertTrue(form_obj.is_valid())

        form = form_to_dict(form_obj)
        self.assertEqual(form['fields'][0]['value'], 'admin')
        self.assertEqual(form['fields'][1]['value'], 42)
