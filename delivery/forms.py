from django import forms


class ProjectUpdateForm(forms.Form):

    update_text = forms.CharField(
        label="Project Update",
        widget=forms.Textarea(
            attrs={
                "rows": 7,
                "placeholder": (
                    "Paste a chat or email update here..."
                ),
                "style": (
                    "width:100%;"
                    "padding:12px;"
                    "border-radius:8px;"
                    "border:1px solid #ddd;"
                    "font-size:15px;"
                ),
            }
        )
    )