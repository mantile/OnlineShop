document.addEventListener("DOMContentLoaded", function() {
    var menu = document.querySelector('.main-menu');
    var sticky = menu.offsetTop;

    function checkScroll() {
        if (window.pageYOffset > sticky) {
            menu.classList.add("fixed");
        } else {
            menu.classList.remove("fixed");
        }
    }

    // Привязка обработчика события прокрутки
    document.addEventListener("scroll", checkScroll);
});

document.getElementById('switchToRegister').addEventListener('click', function(e) {
    e.preventDefault(); // Отменяем стандартное поведение ссылки
    document.getElementById('loginForm').style.display = 'none'; // Скрываем форму входа
    document.getElementById('registrationPanel').style.display = 'block'; // Показываем форму регистрации
});

document.getElementById('switchToLogin').addEventListener('click', function(e) {
    e.preventDefault(); // Отменяем стандартное поведение ссылки
    document.getElementById('loginForm').style.display = 'block'; // Показываем форму входа
    document.getElementById('registrationPanel').style.display = 'none'; // Скрываем форму регистрации
});