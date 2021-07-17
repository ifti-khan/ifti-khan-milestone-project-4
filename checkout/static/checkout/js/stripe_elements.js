/*
    Core logic and payment flow came from this url address below:
    https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements
    
    CSS came from the url address below: 
    https://stripe.com/docs/js

    Additional help has also come from watching the code institutes stripe section
    videos, from the Django mini project.
*/

/* Getting stripe public key and client secret vars using there id and slicing 
of the first and last characters which are quotation marks. Then setting up stripe
using our stripe public key also creating an instance of stripe and then a
stripe card element with css styling.
*/
let stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
let client_secret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripe_public_key);
let elements = stripe.elements();

/*
This style has been taken from the stripe documentation and modified,
and styled to my style requirements.
*/

let style = {
    base: {
        iconColor: '#000000',
        color: '#000000',
        fontFamily: 'Nunito, Roboto, Open Sans, sans-serif',
        fontSize: '16px',
        textTransform: 'capitalize',
        letterSpacing: '1px',
        fontSmoothing: 'antialiased',
        '::placeholder': {
            color: '#aab7c4',
        },
    },
    invalid: {
        iconColor: '#c00013',
        color: '#c00013',
    }
};

// Creating the card element and applying the style to it
let card = elements.create('card', {
    style: style
});

// Mounting the card instance to the html div using the div id of card-element
card.mount('#card-element');

/* 
This was taken from the stripe documentation and displays a card error
in the card-error div in the html. The error message will display if the user
enters incorrect card details, incomplete card details, invalid expiry date
and more.
*/
card.on('change', ({
    error
}) => {
    let displayError = document.getElementById('card-errors');
    if (error) {
        displayError.textContent = error.message;
    } else {
        displayError.textContent = '';
    }
});