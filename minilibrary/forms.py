from django import forms
from .models import Review


class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5, widget=forms.NumberInput(attrs={
            "placeholder": "Califica del 1 al 5",
            "class": "form-control",

        }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Escribe tu reseña",
        "class": "form-control",
        "rows": 4
    }))


bad_words = ["malo", "mugroso", "estupido", "wey", "gonorrea"]


class ReviewForm(forms.ModelForm):
    would_recommend = forms.BooleanField(
        label="Recomendarias este libro", required=False)

    class Meta:
        model = Review
        fields = ["rating", "text"]
        exclude = ["user", "book"]
        widgets = {
            "rating": forms.NumberInput(attrs={
                "placeholder": "calificacion del 1 al 5",
                "class": "form-control"
            }),
            "text": forms.Textarea(attrs={
                "placeholder": "deja tu reseña padrino",
                "class": "form-control",
                "rows": 4
            })
        }

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating < 1 or rating > 5:
            raise forms.ValidationError(
                "La calificacion debe estar entre 1  y 5 estrellas")
        return rating

    def clan_text(self):
        text = self.cleaned_data["text"]
        for word in bad_words:
            if word in text.lower():
                raise forms.ValidationError(
                    f"Con esas manos abrazas a tu madre, no uses lenguaje ofensivo padrino por favor evita usar: {word} en el enunciado")
        return text

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        text = cleaned_data.get("text") or ""
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError(
                "Si la calificacion es de 1 estrella por favor explica mejor tu reseña padrino")

    def save(self, commit=True):
        review = super().save(commit=False)
        if commit:
            review.save()
        return review
