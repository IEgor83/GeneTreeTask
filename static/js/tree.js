document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-relationship');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const personId = this.dataset.personId;

            if (confirm("Вы уверены, что хотите удалить связь?")) {
                fetch(`/delete_relationship/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()  // Получаем токен CSRF
                    },
                    body: JSON.stringify({
                        person_id: personId,
                    })
                })
                    .then(response => {
                        if (response.ok) {
                            const closestElement = this.closest('summary') || this.closest('li');
                            if (closestElement.tagName === 'SUMMARY') {
                                closestElement.parentElement.parentElement.remove();
                            } else {
                                closestElement.remove();
                            }
                        } else {
                            alert("Ошибка при удалении связи.");
                        }
                    })
                    .catch(error => {
                        console.error("Ошибка:", error);
                        alert("Ошибка при удалении связи.");
                    });
            }
        });
    });

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});
