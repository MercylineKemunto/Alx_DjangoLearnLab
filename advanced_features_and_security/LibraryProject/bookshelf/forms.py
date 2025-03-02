from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if "<script>" in title:  # Prevent XSS injection
            raise forms.ValidationError("Invalid title")
        return title
