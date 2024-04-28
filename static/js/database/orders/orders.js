const $btns_waiting= document.querySelectorAll('.waiting-waiter'),
    $btns_paid= document.querySelectorAll('.paid'),
    $btns_delivered= document.querySelectorAll('.delivered'),
    url= document.getElementById('ajax-url').textContent;

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

// Set the waiting waiter status into false or true according to the action
function setWaiting($btn_waiting, boolean_waiting) {
    /** 
     * Realiza una solicitud AJAX para modificar la opcion de waiting_waiter a true o false.
     * @param {Element} $btn_waiting - La información del elemento que se va a modificar.
     * @param {boolean} boolean_waiting - Si se va a modificar a true o a false.
     */
    boolean_waiting ? boolean_waiting= 'True' : boolean_waiting= 'False';
    order_id= $btn_waiting.id.replace('-waiting-waiter', '');
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'action': 'setWaiting',
            'order_id': order_id,
            'boolean_waiting': boolean_waiting, 
        },
        dataType: 'json',
        success: function(response) {
            document.getElementById(`${order_id}-waiting-waiter-true`).classList.toggle('no-display');
            let waiting_info= document.getElementById(`${order_id}-waiting-waiter-info`);
            if (boolean_waiting== 'True'){
                waiting_info.textContent= waiting_info.textContent.replace('False', 'True');
            }else{
                waiting_info.textContent= waiting_info.textContent.replace('True', 'False');
            };
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert(`There was an error changing the waiting waiter option into ${boolean_waiting}.`);
        }
    });
};

// Set the $btn status into false or true according to the action
function setInto($btn, replacer, action, boolean, error){
    /** 
     * Realiza una solicitud AJAX para modificar la opcion de paid a true o false.
     * @param {Element} $btn - La información del elemento que se va a modificar.
     * @param {String} replacer - El texto que se utiliza en el html como clave para el elemento.
     * @param {String} action - Nombre de accion que se va a mandar al views.
     * @param {boolean} boolean - Si se va a modificar a true o a false.
     * @param {String} error - El texto que se envia al usuario en caso de error.
     */
    boolean ? boolean= 'True' : boolean= 'False';
    order_id= $btn.id.replace(`-${replacer}`, '');
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            csrfmiddlewaretoken: getCookie('csrftoken'),
            'action': action,
            'order_id': order_id,
            'boolean': boolean, 
        },
        dataType: 'json',
        success: function(response) {
            let info= document.getElementById(`${order_id}-${replacer}-info`);
            if (boolean== 'True'){
                info.textContent= info.textContent.replace('False', 'True');
            }else{
                info.textContent= info.textContent.replace('True', 'False');
            };
        },
        error: function(xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText);
            alert(error);
        }
    });
};

// EVENTS LISTENERS
// Add event listener to every waiting waiter btn
$btns_waiting.forEach($btn_waiting=>{
    $btn_waiting.addEventListener('change', e=>{
        if ($btn_waiting.checked){
            setWaiting($btn_waiting, true);
        } else{
            setWaiting($btn_waiting, false);
        };
    });
});

// Add event listener to every paid btn
$btns_paid.forEach($btn_paid=>{
    $btn_paid.addEventListener('change', e=>{
        if ($btn_paid.checked){
            setInto($btn_paid, 'paid', 'setPaid', true, `There was an error changing the paid option into true`);
        } else{
            setInto($btn_paid, 'paid', 'setPaid', false, `There was an error changing the paid option into false`);
        };
    });
});

// Add event listener to every delivered btn
$btns_delivered.forEach($btn_delivered=>{
    $btn_delivered.addEventListener('change', e=>{
        if ($btn_delivered.checked){
            setInto($btn_delivered, 'delivered', 'setDelivered', true, `There was an error changing the delivered option into true`);
        } else{
            setInto($btn_delivered, 'delivered', 'setDelivered', false, `There was an error changing the delivered option into false`);
        };
    });
});