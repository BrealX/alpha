from django import forms
from .models import *
from django.utils.translation import gettext as _


class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, label=_("Отзыв"))
    score = forms.IntegerField(label=_("Оценка"), min_value=1, max_value=5)


    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Review
        fields = ['score', 'text', ]

        widgets = {
            'text': forms.Textarea(
                attrs={'rows': 3, 'placeholder': _('Комментарий')}),
        }
