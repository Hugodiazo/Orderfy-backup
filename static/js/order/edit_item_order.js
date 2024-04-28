const d= document;

const q_checkbox_all= d.querySelectorAll('.q-checkbox'),
    quantities= d.querySelectorAll('.q-input'),
    item_quantity= d.getElementById('item-quantity'),
    item_price= d.getElementById('item-price'),
    submit_btn= d.getElementById('submit'),
    item_price_input= d.getElementById('item-price-input');

// If the remove/add checkbox is changed, the quantity input is showed, otherwise, the quantity input is hidden and the price is changed accordingly
const displayQuantityInfo= (added_removed, quantity_info, started)=>{
    // If the checkbox is checked the quantity input is showed, otherwise, the quantity input is hidden
    if (added_removed){
        quantity_info.forEach(info=>{
            info.style.setProperty("display", "block"); 
            if (info.classList.contains('q-input')){
                if (!started){
                    info.value= 1;
                };
                info.min= 1;
            };
            change_item_price(item_price, item_quantity, quantities);
        });
    } else{
        quantity_info.forEach(info=>{
            info.style.setProperty("display", "none"); 
            if (info.classList.contains('q-input')){
                info.value= 0;
                info.min= 0;
            };
            change_item_price(item_price, item_quantity, quantities);
        });
    };
};

const change_item_price= (item_price, item_quantity, quantities)=>{
    item_price.textContent= `${(item_price.getAttribute('data-price') * item_quantity.value).toFixed(2)}$`;

    quantities.forEach(quantity=>{
        let ingredient_price= d.getElementById(quantity.id.replace('quantity-', 'ingredient-price-'));
        ingredient_price.setAttribute('data-price', (ingredient_price.getAttribute('data-unique-price') * item_quantity.value).toFixed(2));

        change_ingredient_price(ingredient_price, quantity);
        if(quantity.value!= 0){
            if(ingredient_price.id.slice(0, 6) == 'remove'){
                item_price.textContent= (parseFloat(item_price.textContent.replace('$', '')) - parseFloat(ingredient_price.textContent.replace('-', '').replace('$', ''))).toFixed(2);
            }else{
                item_price.textContent= (parseFloat(item_price.textContent.replace('$', '')) + parseFloat(ingredient_price.textContent.replace('-', '').replace('$', ''))).toFixed(2);
            };
        };
    });
};

const change_ingredient_price= (ingredient_price, quantity) =>{
    // The prices are changed bassed on the amount of ingredients added/removed
    if(quantity.value!= 0){
        if(ingredient_price.id.slice(0, 6) == 'remove'){
            ingredient_price.textContent= `- ${(ingredient_price.getAttribute('data-price') * quantity.value).toFixed(2)}$`;
        }else{
            ingredient_price.textContent= `${(ingredient_price.getAttribute('data-price') * quantity.value).toFixed(2)}$`;
        };
    } else{
        if(ingredient_price.id.slice(0, 6) == 'remove'){
            ingredient_price.textContent= `- ${ingredient_price.getAttribute('data-price')}$`;
        }else{
            ingredient_price.textContent= `${ingredient_price.getAttribute('data-price')}$`;
        };
    };
};

q_checkbox_all.forEach(q_checkbox=>{
    displayQuantityInfo(q_checkbox.checked, d.querySelectorAll(`#${q_checkbox.id.replace('q-checkbox-', 'quantity-')}`), true);
    q_checkbox.addEventListener('change', e=>{
        displayQuantityInfo(q_checkbox.checked, d.querySelectorAll(`#${q_checkbox.id.replace('q-checkbox-', 'quantity-')}`), false);
    });
});

// If the quantity of ingredients added/deleted is changed, the prices are changed accordingly
quantities.forEach(quantity=>{
    let ingredient_price= d.getElementById(quantity.id.replace('quantity-', 'ingredient-price-'));
    change_ingredient_price(ingredient_price, quantity);
    change_item_price(item_price, item_quantity, quantities);
    quantity.addEventListener('change', e=>{
        let ingredient_price= d.getElementById(quantity.id.replace('quantity-', 'ingredient-price-'));
        change_ingredient_price(ingredient_price, quantity);
        change_item_price(item_price, item_quantity, quantities);
    });
});

// If the amount of items is changed, the total price and the ingredients price is changed accordingly 
change_item_price(item_price, item_quantity, quantities);
item_quantity.addEventListener('change', e=>{
    change_item_price(item_price, item_quantity, quantities);
});

// If the submit button is clicked, the price of the input is updated
submit_btn.addEventListener('click', e=>{
    item_price_input.value= item_price.textContent.replace('$', '');
});
