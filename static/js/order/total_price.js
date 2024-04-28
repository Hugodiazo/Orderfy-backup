const d= document;

const prices= d.querySelectorAll('.item-price'),
    total_price= d.getElementById('total-price');

let total= 0;
prices.forEach(price=>{
    total+= parseFloat(price.textContent.replace('$', ''));
});
total_price.insertAdjacentText('beforeend', `${total.toFixed(2)}$`);