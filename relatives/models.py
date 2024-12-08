from django.db import models

GENDER_CHOICES = [
    ('M', 'Мужской'),
    ('F', 'Женский'),
]

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Relationship(models.Model):
    person = models.ForeignKey(Person, related_name='children', on_delete=models.CASCADE, default=None)
    parent = models.ForeignKey(Person, related_name='parents', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.person} - {self.parent}"


def get_family_tree(person):
    """Строит дерево семьи для указанного человека."""

    parents = Relationship.objects.filter(person=person).values_list('parent', flat=True)
    siblings = (
        Person.objects.filter(
            id__in=Relationship.objects.filter(parent_id__in=parents).values_list('person', flat=True)
        )
        .exclude(id=person.id)
    )

    tree = {
        "person": person,
        "siblings": [
            {"sibling": sibling, "relation": "Брат" if sibling.gender == "M" else "Сестра"} for sibling in siblings
        ],
        "parents": [],
    }

    relationships = Relationship.objects.filter(person=person)
    for rel in relationships:
        if rel.parent:
            parent_role = "Отец" if rel.parent.gender == "M" else "Мать"
            parent_tree = get_family_tree(rel.parent)
            parent_tree["relation"] = parent_role
            tree["parents"].append(parent_tree)

    return tree


def get_descendant_tree(person):
    """
    Строит дерево потомков для указанного человека.

    Аргументы:
        person: Объект Person, для которого строится дерево потомков.

    Возвращает:
        Словарь с информацией о человеке и его потомках.
    """
    children = Person.objects.filter(
        id__in=Relationship.objects.filter(parent=person).values_list('person', flat=True)
    )

    tree = {
        "person": person,
        "relation": None,  # Это корень дерева, поэтому связь не указывается
        "children": [],
    }

    # Добавляем детей рекурсивно
    for child in children:
        child_role = "Сын" if child.gender == "M" else "Дочь"
        child_tree = get_descendant_tree(child)
        child_tree["relation"] = child_role
        tree["children"].append(child_tree)

    return tree


def has_cycle(person, target):
    """
    Проверяет, существует ли цикл в графе родственных связей.
    :param person: Объект Person, от которого начинается проверка.
    :param target: Целевой объект Person, которого проверяем.
    :return: True, если цикл существует; иначе False.
    """
    visited = set()

    def dfs(current):
        if current.id in visited:
            return False
        visited.add(current.id)

        if current.id == target.id:
            return True

        for relationship in current.children.all():
            if dfs(relationship.parent):
                return True

        return False

    return dfs(person)

