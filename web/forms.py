from django import forms
from web.models import Categoria, Libro, Tipo

class CategoriaForm(forms.Form):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Categorías",
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'})

 )
    
class LibroForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=True,
        empty_label="Categoría",
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    tipo = forms.ModelChoiceField(
        queryset=Tipo.objects.all(),
        required=True,
        empty_label="Tipo",
        widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Libro
        fields = ["nombre", "autor", "isbn", "categoria", "tipo"]
        labels = {
            "nombre": "Nombre",
            "autor": "Autor(a)",
            "isbn": "ISBN",
            "categoria": "Categoría",
            "tipo": "Tipo"
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
            "autor": forms.TextInput(attrs={"placeholder": "Autor(a)", "class": "form-control"}),
            "isbn": forms.TextInput(attrs={"placeholder": "ISBN", "class": "form-control"}),}

