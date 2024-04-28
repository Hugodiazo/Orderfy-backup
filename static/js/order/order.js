// Constantes que almacenan todos los botones de aumento y disminución, y la URL de la solicitud AJAX
const all_increase_btns = document.querySelectorAll('.increase-btn');
const all_decrease_btns = document.querySelectorAll('.decrease-btn');
const url = document.getElementById('ajax-url').textContent;

// Obtener el token CSRF de la cookie
function getCookie(name) {
    /**
     * Obtiene el valor de una cookie por su nombre.
     * @param {string} name - El nombre de la cookie que se desea obtener.
     * @returns {string|null} El valor de la cookie o null si no se encuentra.
     */
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Busca el token CSRF en la cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            };
        };
    };
    return cookieValue;
};

// Obtener el precio unitario de un producto
function get_unity_price(data_item){
    const hex_byte= data_item.match(/.{1,2}/g).map(byte => parseInt(byte, 16)),
        json_string= new TextDecoder().decode(new Uint8Array(hex_byte)),
        json_element= JSON.parse(json_string),
        unity_price= parseFloat(document.getElementById(`${json_element.id}-unity-price`).textContent.replace('Unity price=', '').replace('$', ''));

        return unity_price;
};

function update_total_price(price_inputs, total_price_input){
    let total_price= 0;
    price_inputs.forEach(price_input=>{
        item_price= parseFloat(price_input.textContent.replace('$', ''));
        total_price+= item_price;
    });
    total_price_input.textContent= `Total price: ${total_price.toFixed(2)}$`;
};

// Eliminar un elemento del pedido
function delete_order_item(data_item){
    /** 
     * Realiza una solicitud AJAX para eliminar un elemento del pedido.
     * @param {string} data_item - La información del elemento que se va a eliminar.
     */
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'action': 'delete_order_item',
            'item_info': data_item,
        },
        dataType: 'json',
        success: function(response) {
            let divToRemove = document.getElementById(response.order_item_id);
            divToRemove.parentNode.removeChild(divToRemove);
            let price_inputs= document.querySelectorAll('.item-price'),
                total_price_input= document.getElementById('total-price');
            update_total_price(price_inputs, total_price_input);
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert('There was an error deleting the item from the order.');
        }
    });
};

// Función para cambiar la cantidad de un elemento en el carrito
function change_quantity(increase, btn){
    /**
     * Cambia la cantidad de un elemento en el carrito.
     * @param {boolean} increase - Indica si se debe aumentar la cantidad (true) o disminuirla (false).
     * @param {HTMLElement} btn - El botón que activó la acción de cambio de cantidad.
     */
    const data_item= btn.getAttribute('data-item'),
        quantity_element= document.getElementById(`${data_item}-quantity`),
        quantity= parseInt(quantity_element.textContent.replace('Quantity:', '')),
        price_element= document.getElementById(`${data_item}-price`),
        price= parseFloat(price_element.textContent.replace('$', '')),
        unity_price= get_unity_price(data_item),
        price_inputs= document.querySelectorAll('.item-price'),
        total_price_input= document.getElementById('total-price');

    // Función para realizar una solicitud AJAX para cambiar la cantidad del elemento
    function ajax_change_quantity(action){
        /**
         * Realiza una solicitud AJAX para cambiar la cantidad del elemento en el carrito.
         * @param {string} action - La acción a realizar, 'increase' para aumentar o 'decrease' para disminuir la cantidad.
         */
        $.ajax({
            url: url,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: getCookie('csrftoken'),
                'action': 'change_quantity',
                'item_info': btn.getAttribute('data-item'),
                'btn': action,
            },
            dataType: 'json',
            success: function(response) {
                if (action== 'increase'){
                    quantity_element.textContent= `Quantity: ${quantity+1}`;
                    price_element.textContent= `${parseFloat(price+unity_price).toFixed(2)}$`;
                } else{
                    quantity_element.textContent= `Quantity: ${quantity-1}`;
                    price_element.textContent= `${parseFloat(price-unity_price).toFixed(2)}$`;
                };
                update_total_price(price_inputs, total_price_input);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                alert('There was an error changing the quantity.');
            }
        });
    };

    // Lógica para determinar la acción a realizar y llamar a la función de solicitud AJAX correspondiente
    if(increase){
        ajax_change_quantity('increase', quantity_element, btn);
    }else{
        if (quantity-1 == 0){
            if(confirm('Do you want to delete this menu item from the order?')){
                delete_order_item(data_item);
            };
        } else{
            ajax_change_quantity('decrease', quantity_element, btn);
        };
    };
};

// Manejadores de eventos al cargar el documento
$(document).ready(function() {
    // Manejador de eventos para todos los botones de aumento
    all_increase_btns.forEach(increase_btn=>{
        increase_btn.addEventListener('click', e=>{
            change_quantity(true, e.target);
        });
    });   

    // Manejador de eventos para todos los botones de disminución
    all_decrease_btns.forEach(decrease_btn=>{
        decrease_btn.addEventListener('click', e=>{
            change_quantity(false, e.target);
        });
    });
    
    // Manejador de eventos para boton de eliminar item

});
