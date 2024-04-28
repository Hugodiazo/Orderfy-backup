const $add_btns= document.querySelectorAll('.add-link');

$add_btns.forEach($add_btn=>{
    $add_btn.addEventListener('click', e=>{
        window.location.href= $add_btn.getAttribute('data-link');
    });
});