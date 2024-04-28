let del_btns= document.querySelectorAll('.del_btn');

del_btns.forEach(del_btn=>{
    del_btn.addEventListener('click', e=>{
        if (!confirm("Are you sure you want to delete it?")) {
            e.preventDefault();
        };
    });
});