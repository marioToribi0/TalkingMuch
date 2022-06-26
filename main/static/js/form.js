
var form_size = document.querySelector("#id_size");
var count = 1;

// Identify
var string = "";
var value = 4;
var lastString = "col-lg-3";
let selects = document.querySelectorAll('.options select');

// First time
count = form_size.value;
    
if (count<4){
    string = `col-lg-${12/count}`;
}

let div_options = document.querySelectorAll(`.options div.${lastString}`)
for (let i=0; i<div_options.length; i++){
    div_options[i].classList.remove(lastString);
    div_options[i].classList.add(string);
    
    if (i>count-1){
        div_options[i].style.display='none';
    }
    else{
        div_options[i].style.display='block';
    }
}
lastString = string;


form_size.addEventListener('change', function(){
    count = form_size.value;
    
    if (count<4){
        string = `col-lg-${12/count}`;
    }
    else{
        string = 'col-lg-4';
    }
    let div_options = document.querySelectorAll(`.options div.${lastString}`)
    
    for (let i=0; i<div_options.length; i++){
        div_options[i].classList.remove(lastString);
        div_options[i].classList.add(string);
        
        if (i>count-1){
            div_options[i].style.display='none';
        }
        else{
            div_options[i].style.display='block';
        }
        // Show new info
        if (i<count){
            if (['2','3','4'].includes(selects[i].value)){
                div = document.querySelector(`#option_${selects[i].value}`);
                div.hidden = false;
            }
        }

    }
    lastString = string;

    // Hidden select
    for (let i=0; i<selects.length; i++){
        for (let j=0; j<7; j++){
            if (j<count && j!=i){
                selects[i].options[j].hidden = true;
            }
            else{
                selects[i].options[j].hidden = false;
            }
        }
    }


});



// Add events listener
let last_value = ['1','2','3','4','5','6','7'];

for (let i=0; i<selects.length; i++){
    selects[i].addEventListener('change', function(){
        let actual_value = selects[i].value;
        for (let j=0;j<selects.length; j++){
            if (j!=i){
                selects[j].options[parseInt(actual_value)-1].hidden = true;
                selects[j].options[parseInt(last_value[i])-1].hidden = false;
            }
        }
        // Conditionals

        if (['2','3','4'].includes(actual_value)){
            div = document.querySelector(`#option_${actual_value}`);
            div.hidden = false;
        }
        if (['2','3','4'].includes(last_value[i])){
            div = document.querySelector(`#option_${last_value[i]}`);
            div.hidden = true;
        }
        last_value[i] = actual_value;
    })
}

// Conditionals
// Hidden divs first
['2','3','4'].forEach(function(el){
    div = document.querySelector(`#option_${el}`);
    div.hidden = true;
})