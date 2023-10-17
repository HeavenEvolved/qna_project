var date_button = document.querySelectorAll('.date');
var option_button = document.querySelectorAll('.option');
var desc_button = document.querySelectorAll('.desc');

if (date_button)
date_button.forEach((date) => {
    date.addEventListener('click', (e) => {
        if (date.classList.contains('selected')) $(date).removeClass('selected');
        else {
            $('.date.selected').removeClass('selected');
            $(date).addClass('selected');
        }
    });
});

if (option_button)
option_button.forEach((option) => {
    option.addEventListener('click', (e) => {
        if (option.classList.contains('selected')) $(option).removeClass('selected');
        else {
            $('.option.selected').removeClass('selected');
            $(option).addClass('selected');
        }
    });
});

if (desc_button)
desc_button.forEach((desc) => {
    desc.addEventListener('click', (e) => {
        if (desc.classList.contains('selected')) $(desc).removeClass('selected');
        else {
            $('.desc.selected').removeClass('selected');
            $(desc).addClass('selected');
        }
    });
});