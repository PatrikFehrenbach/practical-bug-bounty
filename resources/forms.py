from django import forms
from django_select2.forms import Select2MultipleWidget
from .models import Tag

class ImportMediumForm(forms.Form):
    article_urls = forms.CharField(widget=forms.Textarea(attrs={'rows': 10}), label="Medium Article URLs (One per line)")
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget(attrs={'data-placeholder': 'Select tags'}),
        label="Tags for these Articles"
    )
