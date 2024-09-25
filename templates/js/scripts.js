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

const button = document.getElementById('add-to-cart-button');
if (button) {
    button.addEventListener('click', function() {
        const productId = this.dataset.productId;  // Предполагается, что у кнопки есть атрибут data-product-id

        $.ajax({
            url: '/orders/add-to-cart/' + productId + '/',
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken, // Передавайте CSRF-токен
            },
            success: function(response) {
                if (response.success) {
                    alert('Товар добавлен в корзину! Общее количество: ' + response.total_quantity);
                } else {
                    alert('Ошибка: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Произошла ошибка при добавлении товара в корзину.');
            }
        });
    });
}
