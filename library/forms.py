from django import forms

from .models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book_id', 'reviewer')
        widgets = {'book_id': forms.HiddenInput(),
                   'reviewer': forms.HiddenInput()}

