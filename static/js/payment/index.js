const $pay_now_btn= document.getElementById('pay-now-btn'),
    $pay_now= document.querySelectorAll('.pay-now-toggled');

$pay_now_btn.addEventListener('click', e=>{
    $pay_now.forEach($now_btn=>{
        $now_btn.classList.toggle('not-shown');
    });
});