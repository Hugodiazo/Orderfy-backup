const d= document;

const displayRemovablePriceInfo= (removable, info)=>{
    // If the checkbox is checked then the price input is showed, otherwise, the price input is hidden
    let priceInfo= d.querySelectorAll(info);

    if (removable){
        priceInfo.forEach(info=>{
            info.style.setProperty("display", "block"); 
        });
    } else{
        priceInfo.forEach(info=>{
            info.style.setProperty("display", "none"); 
        });
    };
};

let removableCheckbox= d.getElementById("removable"),
    removable= removableCheckbox.checked,
    addableCheckbox= d.getElementById("addable"),
    addable= addableCheckbox.checked;

displayRemovablePriceInfo(removable, ".r_price_info");
displayRemovablePriceInfo(addable, ".a_price_info");

removableCheckbox.addEventListener('change', e=>{
    removable= removableCheckbox.checked;
    displayRemovablePriceInfo(removable, '.r_price_info');
});
addableCheckbox.addEventListener('change', e=>{
    addable= addableCheckbox.checked;
    displayRemovablePriceInfo(addable, '.a_price_info');
});