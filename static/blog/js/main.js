// JavaScript код
document.addEventListener('DOMContentLoaded', function() {
    var likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var postId = this.getAttribute('data-post-id');
            var likeCountElement = this.nextElementSibling;

            fetch('/like-post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Получаем CSRF-токен из куки
                },
                body: JSON.stringify({ post_id: postId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked) {
                    likeCountElement.textContent = data.likes_count;
                    // Обновляем интерфейс, например, меняем цвет кнопки или иконку
                    // ...
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        });
    });

    // Функция для получения CSRF-токена из куки
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Получаем CSRF-токен из куки
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



document.addEventListener("DOMContentLoaded", function() {
                    var commentForms = document.querySelectorAll('.transparent-form');

                    commentForms.forEach(function(form) {
                        var commentField = form.querySelector('textarea');
                        var publishButton = form.querySelector('.publish-button');

                        // Функция для отображения/скрытия кнопки "Опубликовать"
                        function togglePublishButton() {
                            if (commentField.value.trim() !== '') {
                                publishButton.style.display = 'inline'; // Показываем кнопку
                            } else {
                                publishButton.style.display = 'none'; // Скрываем кнопку
                            }
                        }

                        // Следим за изменениями в текстовом поле
                        commentField.addEventListener('input', togglePublishButton);

                        // Инициализация состояния кнопки при загрузке страницы
                        togglePublishButton();
                    });
                });