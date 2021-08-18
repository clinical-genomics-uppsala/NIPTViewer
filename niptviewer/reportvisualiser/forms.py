from django import forms


class SearchResult(forms.Form):
    search_data = forms.CharField(label='search for flowcell or sample', max_length=100)


class UploadFileForm(forms.Form):
    file = forms.FileField()
