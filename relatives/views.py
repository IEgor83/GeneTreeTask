import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from relatives.forms import PersonForm
from relatives.models import Person, Relationship, get_family_tree, get_descendant_tree


def person_list(request) -> render:
    """
    Отображает список всех людей.

    args:
        request: HTTP запрос, содержащий информацию о запросе.
    return:
        render: Рендерит страницу с перечнем всех людей.
    """
    people = Person.objects.all()
    return render(request, 'relatives/people_list.html', {'people': people})


def person_detail(request, person_id: int) -> render:
    """
    Отображает детальную информацию о человеке, а также форму для редактирования данных.

    args:
        request: HTTP запрос, содержащий информацию о запросе.
        person_id: ID человека, информацию о котором необходимо отобразить.
    return:
        render: Рендерит страницу с данными человека и форму редактирования.
    """
    person = get_object_or_404(Person, id=person_id)
    parent_tree = get_family_tree(person)
    child_tree = get_descendant_tree(person)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_detail', person_id=person.id)
    else:
        form = PersonForm(instance=person)

    return render(request, 'relatives/person_detail.html', {
        'person': person,
        'form': form,
        'family_tree': parent_tree,
        'child_tree': child_tree,
    })


def person_add(request) -> render:
    """
    Добавляет нового человека. Если запрос POST, сохраняет данные формы и перенаправляет на страницу подробностей.

    args:
        request: HTTP запрос, содержащий информацию о запросе.
    return:
        render: Рендерит страницу с формой добавления нового человека.
    """
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save()
            return redirect('person_detail', person_id=person.id)
    else:
        form = PersonForm()

    return render(request, 'relatives/add_person.html', {'form': form})


@csrf_exempt
def delete_relationship(request) -> JsonResponse:
    """
    Удаляет связь с родителями для указанного человека. Ожидает POST запрос с телом JSON, содержащим ID человека.

    args:
        request: HTTP запрос, содержащий данные для удаления связи.
    return:
        JsonResponse: Ответ с результатом выполнения операции (успех или ошибка).
    """
    if request.method == "POST":
        data = json.loads(request.body)
        person_id = data.get('person_id')

        try:
            Relationship.objects.filter(parent_id=person_id).delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Неверный метод запроса"}, status=405)


def delete_person(request, person_id: int) -> redirect:
    """
    Удаляет человека и его связи с другими людьми. После успешного удаления перенаправляет на страницу списка людей.

    args:
        request: HTTP запрос, содержащий информацию о запросе.
        person_id: ID человека, которого необходимо удалить.
    return:
        redirect: Перенаправление на страницу списка людей.
    """
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        Relationship.objects.filter(person=person).delete()
        Relationship.objects.filter(parent=person).delete()

        person.delete()
        messages.success(request, f'Человек {person} был успешно удалён.')

        return redirect('person_list')
