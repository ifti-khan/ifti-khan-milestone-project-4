// Getting the element using id and storing it var called countrySelected
let countrySelected = $('#id_default_country').val();

// If a country is not selected then the text color will be #797979 which is a grey colour
if(!countrySelected) {
    $('#id_default_country').css('color', '#797979');
};

/* This is for if a country is selected what will happen is that the
selected colour will be black and if not selected then it will be #797979 which is a grey colour*/
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#797979');
    } else {
        $(this).css('color', '#000000');
    }
});