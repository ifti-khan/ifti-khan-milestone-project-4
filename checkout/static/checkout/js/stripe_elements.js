/*
    Core logic and payment flow came from this url address below:
    https://stripe.com/docs/payments/accept-a-payment?platform=web&ui=elements
    
    CSS came from the url address below: 
    https://stripe.com/docs/js
    https://stripe.com/docs/payments/accept-a-payment

    Additional help has also come from watching the code institutes stripe section
    videos, from the Django mini project.
*/

/* Getting stripe public key and client secret vars using there id and slicing 
of the first and last characters which are quotation marks. Then setting up stripe
using our stripe public key also creating an instance of stripe and then a
stripe card element with css styling.
*/
let stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
let clientSecret = $('#id_client_secret').text().slice(1, -1);
let stripe = Stripe(stripePublicKey);
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

/* Realtime validation card error
This was taken from the stripe documentation and modified and this displays a card error
in the card-error div in the html. The error message will display if the user
enters incorrect card details, incomplete card details, invalid expiry date
and more.
*/
card.on('change', ({
    error
}) => {
    /* This is for the card error div within the checkout html file
    that will display the stripe error messages */
    let displayError = document.getElementById('card-errors');
    if (error) {
        let html =
            `<span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${error.message}</span>`;
        $(displayError).html(html);
    } else {
        displayError.textContent = '';
    }
});

/* Form submit handling
This code below
*/
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    // prevents the form from submitting
    ev.preventDefault();

    /* Disabling both the card element and submit button to 
    avoid multiple card submissions*/
    card.update({
        'disabled': true
    });
    $('#submit-button').attr('disabled', true);

    // This is for the spinner overlay, for when a payment is being processed
    $('#payment-form').fadeToggle(100);
    $('#spinner-overlay').fadeToggle(100);

    /* Getting save delivery info checkbox value and other form data
    and posting it to the cache_checkout_data view*/
    let saveInfo = Boolean($('#id-save-del-info').attr('checked'));
    // From using {% csrf_token %} in the form
    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    let postData = {
        'csrfmiddlewaretoken': csrfToken,
        'client_secret': clientSecret,
        'save_info': saveInfo,
    };
    let url = '/checkout/cache_checkout_data/';

    // posting the data to the view using jQuery post method
    $.post(url, postData).done(function () {

        // Calling the confirm card payment method
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                /* Getting all the billing, address, shipping details from 
                the order form and trimming off any white space*/
                billing_details: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    email: $.trim(form.email_address.value),
                    address: {
                        line1: $.trim(form.address_line1.value),
                        line2: $.trim(form.address_line2.value),
                        city: $.trim(form.town_or_city.value),
                        state: $.trim(form.county.value),
                        country: $.trim(form.country.value),
                    }
                }
            },
            shipping: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                address: {
                    line1: $.trim(form.address_line1.value),
                    line2: $.trim(form.address_line2.value),
                    city: $.trim(form.town_or_city.value),
                    state: $.trim(form.county.value),
                    postal_code: $.trim(form.postcode.value),
                    country: $.trim(form.country.value),

                }
            },
            // Executing the result function
        }).then(function (result) {
            /* This is for the card error div within the checkout html file
            that will display the stripe error messages */
            let displayError = document.getElementById('card-errors');
            if (result.error) {
                let html =
                    `<span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
            <span>${result.message}</span>`;
                $(displayError).html(html);

                // This is for the spinner overlay, for when a payment is being processed
                $('#payment-form').fadeToggle(100);
                $('#spinner-overlay').fadeToggle(100);

                // Enabling the card element and submit button if there is an error
                card.update({
                    'disabled': false
                });
                $('#submit-button').attr('disabled', false);
            } else {
                // If status is success then the form will be submitted 
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
        });
    }).fail(function () {
        // just reload the page, the error will be in django messages
        location.reload();
    })
});