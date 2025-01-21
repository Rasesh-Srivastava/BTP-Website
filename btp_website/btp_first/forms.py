from django import forms

class PlayerForm(forms.Form):
    player1 = forms.CharField(
        label='Player 1',
        max_length=1,
        widget=forms.PasswordInput(attrs={'placeholder': 'Player 1', 'class': 'form-control'}),
    )
    player2 = forms.CharField(
        label='Player 2',
        max_length=1,
        widget=forms.PasswordInput(attrs={'placeholder': 'Player 2', 'class': 'form-control'}),
    )
