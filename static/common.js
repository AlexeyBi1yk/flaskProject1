// Ожидаем, пока загрузится вся страница
$(document).ready(function () {
    // Обработчик события отправки формы
    $(".search-form").submit(function (event) {
        // Предотвращаем стандартное поведение браузера (перезагрузку страницы)
        event.preventDefault();

        // Получаем данные формы
        var formData = $(this).serialize();

        // Отправляем AJAX-запрос
        $.ajax({
            type: "GET", // Метод запроса
            url: $(this).attr("action"), // URL для отправки запроса
            data: formData, // Данные формы
            success: function (response) {
                // Обновляем содержимое страницы
                $("#content").html(response);
            }
        });
    });
});
