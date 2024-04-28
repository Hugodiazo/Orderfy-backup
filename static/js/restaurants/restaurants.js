document.addEventListener("DOMContentLoaded", function() {
    const openPopupButton = document.getElementById("open-popup");
    const overlay = document.getElementById("overlay");
    const popup = document.getElementById("popup-Bene");
    const btnCerrarPopup = document.getElementById("btn-cerrar-popup")

    openPopupButton.addEventListener("click", function() {
        overlay.classList.add("active");
        popup.classList.add("active");
        btnCerrarPopup.classList.add("active");
    });

    overlay.addEventListener('click', function(e){
        if (e.target == overlay){
            overlay.classList.remove('active');
            popup.classList.remove('active');
            btnCerrarPopup.classList.remove('active');
        }
    })

    btnCerrarPopup.addEventListener("click", function() {
        overlay.classList.remove("active");
        popup.classList.remove("active");
        btnCerrarPopup.classList.remove("active");
    });

});