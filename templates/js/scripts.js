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

document.getElementById('checkout-button').addEventListener('click', function() {
    console.log('Кнопка нажата!'); // Добавьте это сообщение для отладки

    fetch('/orders/create_order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            window.location.href = '/orders/orders/'; // Перенаправление при успехе
        } else {
            alert('Ошибка при оформлении заказа.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error); // Сообщите об ошибке в консоли
    });
});

function updateSubtotal(productId, quantity) {
    const unitPrice = parseFloat(document.querySelector(`.unit-price[data-price][data-product-id="${productId}"]`).dataset.price);
    const subtotal = quantity * unitPrice;
    document.querySelector(`.subtotal[data-product-id="${productId}"]`).textContent = subtotal.toFixed(2); // Обновление итого
}


error: function(xhr) {
    console.error(xhr);  // Логируем весь объект xhr для просмотра
    try {
        var errorMessage = xhr.responseJSON.message || 'Неизвестная ошибка';
        alert('Ошибка при оформлении заказа: ' + errorMessage);
    } catch (e) {
        alert('Ошибка при оформлении заказа: Неизвестная ошибка');
    }
}

document.addEventListener('DOMContentLoaded', function(){
    const checkoutButton = document.getElementById('checkout-button');
    if (checkoutButton) {
        checkoutButton.addEventListener('click', function() {
            console.log('Кнопка нажата!'); // Добавьте это сообщение для отладки

            fetch('/orders/create_order/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    window.location.href = '/orders/orders/'; // Перенаправление при успехе
                } else {
                    alert('Ошибка при оформлении заказа.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error); // Сообщите об ошибке в консоли
            });
        });
    }

    document.querySelectorAll('.quantity-decrease, .quantity-increase').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;
            const input = document.querySelector(`input[data-product-id="${productId}"]`);
            let quantity = parseInt(input.value);

            if (this.classList.contains('quantity-increase')) {
                quantity++;
            } else if (this.classList.contains('quantity-decrease')) {
                if (quantity > 1) {
                    quantity--;
                }
            }

            input.value = quantity; // Обновление поля ввода
            updateSubtotal(productId, quantity); // Обновление суммы товара
        });
    });
});