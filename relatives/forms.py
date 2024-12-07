from django import forms

from relatives.models import Person, Relationship, GENDER_CHOICES, has_cycle


class PersonForm(forms.ModelForm):
    parent_1 = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        label="Родитель 1",
        empty_label="Выбрать",
    )
    parent_2 = forms.ModelChoiceField(
        queryset=Person.objects.all(),
        required=False,
        label="Родитель 2",
        empty_label="Выбрать",
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label="Пол",
        required=True,
        widget=forms.Select(attrs={"placeholder": "Выбрать"})
    )

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'middle_name', 'gender']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'middle_name': 'Отчество',
            'gender': 'Пол',
        }

    def __init__(self, *args, **kwargs):
        self.person = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if self.person:
            self.fields['parent_1'].queryset = Person.objects.exclude(id=self.person.id)
            self.fields['parent_2'].queryset = Person.objects.exclude(id=self.person.id)

        relationships = Relationship.objects.filter(person=self.person)
        parent_1 = relationships.filter(parent__gender='M').first()
        parent_2 = relationships.filter(parent__gender='F').first()

        self.fields['parent_1'].initial = parent_1.parent if parent_1 else None
        self.fields['parent_2'].initial = parent_2.parent if parent_2 else None

    def clean(self):
        cleaned_data = super().clean()
        parent_1 = cleaned_data.get('parent_1')
        parent_2 = cleaned_data.get('parent_2')

        if not self.person:
            return cleaned_data

        if not (parent_1 and Relationship.objects.filter(person=self.person, parent=parent_1).exists()):
            if parent_1 and has_cycle(parent_1, self.person):
                raise forms.ValidationError(f"Выбор родителя '{parent_1}' создает цикл в дереве.")

        if not (parent_2 and Relationship.objects.filter(person=self.person, parent=parent_2).exists()):
            if parent_2 and has_cycle(parent_2, self.person):
                raise forms.ValidationError(f"Выбор родителя '{parent_2}' создает цикл в дереве.")

        return cleaned_data

    def save(self, commit=True):
        person = super().save(commit=commit)

        parent_1 = self.cleaned_data.get('parent_1')
        parent_2 = self.cleaned_data.get('parent_2')

        Relationship.objects.filter(person=person).delete()

        if parent_1:
            Relationship.objects.create(person=person, parent=parent_1)
        if parent_2:
            Relationship.objects.create(person=person, parent=parent_2)

        return person
