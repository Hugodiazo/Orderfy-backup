const $back_btn= document.getElementById('back-btn');

$back_btn.addEventListener('click', e=>{
    if (confirm('Are you sure you want to go back?, the order is not going to be confirmed and your information will not be saved.')){
        window.location.href = $back_btn.getAttribute('data-href');
    };
});