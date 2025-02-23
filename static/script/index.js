"use strict";
document.addEventListener("DOMContentLoaded", function () {
  const messages = document.querySelectorAll(".message-notification");

  messages.forEach(function (message) {
    setTimeout(function () {
      message.classList.add("hidden"); // Добавляем класс для плавного исчезновения
      setTimeout(function () {
        message.remove(); // Удаляем элемент из DOM после завершения анимации
      }, 1000); // Ждем 1 секунду (время анимации)
    }, 4000); // Задержка 4 секунды перед началом исчезновения
  });
});
