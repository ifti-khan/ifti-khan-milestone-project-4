# Validation

## HTML5 Validation
I have tested all of the HTML files using the HTML5 W3C validator and got some interesting results. The validator does not seem to recognize Django template language and it showing a large number of errors. 


## CSS3 Validation
Here I have tested all of the CSS files within the project using the CSS3 W3C validator and got one error which was caused by a comma. That error was corrected and the file was validated again with no errors, so all my CSS files pass the CSS£ W3C validation.

### CSS3 Results PDFs
#### Base CSS -> [View PDF](/writeup_files/validation/base_css_validation.pdf)
#### Responsive CSS -> [View PDF](/writeup_files/validation/responsive_css_validation.pdf)
#### Profile CSS -> [View PDF](/writeup_files/validation/profile_css_validation.pdf)
#### Checkout CSS -> [View PDF](/writeup_files/validation/checkout_css_validation.pdf)

## Javascript Validation
Here I have tested my javascript files using an online syntax validator. After checking all of my js files with the syntax checker, all results showed that I had no errors.

### Javascript Results Screenshots
#### Base JS ![Base JS Validation Screenshot](/writeup_files/validation/base_js_validation.jpg)
#### Map JS ![Map JS Validation Screenshot](/writeup_files/validation/map_js_validation.jpg)
#### Countryfield JS ![Countryfield JS Validation Screenshot](/writeup_files/validation/countryfield_js_validation.jpg)
#### Stripe JS ![Stripe JS Validation Screenshot](/writeup_files/validation/stripe_js_validation.jpg)

## Python PEP8 Validation
At the beginning of this project I installed a linter by the name of flake 8 within VSCode and set that as my default linter, this can be seen in the requirements file - flake8==3.9.2 has been installed. Throughout the entire project I made sure my python code was PEP8 compliant by making sure line were not too long, no unused variables and more. 

There is 4 lines of code in the settings file which cannot be made PEP8 complaint and they are to do with the Django password auth.

### PEP8 Screenshot
#### No PEP8 ![No PEP8 Screenshot](/writeup_files/validation/settings_no_pep8.jpg)

## Colour Validation
Here are I checked my colours to make sure that they were web safe compliant, after checking all colours pass and are complaint.

### Colour Validation Screenshots
#### Colour Validation 1 ![Colour Validation 1 Screenshot](/writeup_files/validation/colour_validation_1.jpg)
#### Colour Validation 2 ![Colour Validation 2 Screenshot](/writeup_files/validation/colour_validation_2.jpg)
#### Colour Validation 3 ![Colour Validation 3 Screenshot](/writeup_files/validation/colour_validation_3.jpg)