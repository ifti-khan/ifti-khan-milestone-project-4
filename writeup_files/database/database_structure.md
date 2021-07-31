# User Model
The User model I am using has come from the default Django authentication model and has been used by importing it from django.contrib.auth. For more information about Djangos authentication [click here](https://docs.djangoproject.com/en/3.2/ref/contrib/auth/) to find out more.

# Profile App
## Profile Model
| Name             | Database Key              | Field Type      | Validation                                   |
|------------------|---------------------------|-----------------|----------------------------------------------|
| ---------------- | ------------------------- | --------------- | ------------                                 |
| Full Name        | default_full_name         | CharField       | max_length=50, null=True, blank=True         |
| Email Address    | default_email_address     | EmailField      | max_length=254, null=True, blank=True        |
| Contact Number   | default_phone_number      | CharField       | max_length=20, null=True, blank=True         |
| Address Line 1   | default_address_line1     | CharField       | max_length=80, null=True, blank=True         |
| Address Line 2   | default_address_line2     | CharField       | max_length=80, null=True, blank=True         |
| Town / City      | default_town_or_city      | CharField       | max_length=40, null=True, blank=True         |
| County           | default_county            | CharField       | max_length=80, null=True, blank=True         |
| Postcode         | default_postcode          | CharField       | max_length=20, null=True, blank=True         |
| Country          | default_country           | CountryField    | blank_label='Country', null=True, blank=True |
| User             | user                      | OneToOneField   | User, on_delete=models.CASCADE               |
|                  |                           |                 |                                              |

# Product App
## Category Model
| Name                   | Database Key              | Field Type      | Validation                            |
|------------------------|---------------------------|-----------------|---------------------------------------|
| ----------------       | ------------------------- | --------------- | ------------                          |
| Category Name          | category_name             | CharField       | max_length=254                        |
| Category Friendly Name | category_friendly_name    | CharField       | max_length=254, null=True, blank=True |
|                        |                           |                 |                                       |

## Products Model
| Name                  | Database Key          | Field Type     | Validation                                                   |
|-----------------------|-----------------------|----------------|--------------------------------------------------------------|
| --------------------- | --------------------- | -------------- | ------------                                                 |
| Category              | category              | ForeignKey     | 'Category', null=True, blank=True, on_delete=models.SET_NULL |
| Product Name          | product_name          | CharField      | max_length=254                                               |
| Product Description   | product_description   | TextField      |                                                              |
| Product Price         | product_price         | DecimalField   | max_digits=6, decimal_places=2                               |
| Product Rating        | product_rating        | DecimalField   | max_digits=6, decimal_places=2, null=True, blank=True        |
| SKU                   | sku                   | CharField      | max_length=254, null=True, blank=True                        |
| Product Size          | product_sizes         | BooleanField   | null=True, blank=True                                        |
| Product Image         | product_image         | ImageField     | null=True, blank=True                                        |
| Product Image URL     | product_image_url     | URLField       | max_length=1024, null=True, blank=True                       |
|                       |                       |                |                                                              |

## Review Model
| Name             | Database Key     | Field Type      | Validation                        |
|------------------|------------------|-----------------|-----------------------------------|
| ---------------- | ---------------- | --------------- | ------------                      |
| Product          | product          | ForeignKey      | Product, on_delete=models.CASCADE |
| User             | user             | ForeignKey      | User, on_delete=models.CASCADE    |
| Review Title     | review_title     | CharField       | max_length=250                    |
| Review Rating    | review_rating    | DecimalField    | max_digits=2, decimal_places=1    |
| Review Message   | review_message   | TextField       | max_length=1000                   |
| Review Date      | date_created     | DateTimeField   | auto_now_add=True                 |
| Review Time      | time_created     | DateTimeField   | auto_now_add=True                 |
|                  |                  |                 |                                   |

# Community App
## Question Model
| Name               | Database Key       | Field Type      | Validation                     |
|--------------------|--------------------|-----------------|--------------------------------|
| ------------------ | ------------------ | --------------- | ------------                   |
| User               | user               | ForeignKey      | User, on_delete=models.CASCADE |
| Question Title     | question_title     | CharField       | max_length=250                 |
| Question Message   | question_message   | TextField       | max_length=1000                |
| Question Date      | date_created       | DateTimeField   | auto_now_add=True              |
| Message Time       | time_created       | DateTimeField   | auto_now_add=True              |
|                    |                    |                 |                                |

## Answer Model
| Name            | Database Key    | Field Type      | Validation                         |
|-----------------|-----------------|-----------------|------------------------------------|
| --------------- | --------------- | --------------- | ------------                       |
| Answer ID       | id              | AutoField       | primary_key=True                   |
| Question        | question        | ForeignKey      | Question, on_delete=models.CASCADE |
| User            | user            | ForeignKey      | User, on_delete=models.CASCADE     |
| Answer Message  | answer_message  | TextField       | max_length=1000                    |
| Answer Date     | date_created    | DateTimeField   | auto_now_add=True                  |
| Answer Time     | time_created    | DateTimeField   | auto_now_add=True                  |
|                 |                 |                 |                                    |

# Checkout App
## Order model
| Name                   | Database Key           | Field Type      | Validation                                                                           |
|------------------------|------------------------|-----------------|--------------------------------------------------------------------------------------|
| ---------------------- | ---------------------- | --------------- | ------------                                                                         |
| Order Number           | order_number           | CharField       | max_length=32, null=False, editable=False                                            |
| User Profile           | user_profile           | ForeignKey      | UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders' |
| Full Name              | full_name              | CharField       | max_length=50, null=False, blank=False                                               |
| Email Address          | email_address          | EmailField      | max_length=254, null=False, blank=False                                              |
| Phone Number           | phone_number           | CharField       | max_length=20, null=False, blank=False                                               |
| Address Line 1         | address_line1          | CharField       | max_length=80, null=False, blank=False                                               |
| Address Line 2         | address_line2          | CharField       | max_length=80, null=False, blank=False                                               |
| City / Town            | city_or_town           | CharField       | max_length=40, null=False, blank=False                                               |
| County / State         | county_state           | CharField       | max_length=80, null=True, blank=True                                                 |
| Country                | country                | CharField       | blank_label='Country *', null=False, blank=False                                     |
| Postcode               | postcode               | CharField       | max_length=20, null=True, blank=True                                                 |
| Order Date             | date                   | DateTimeField   | auto_now_add=True                                                                    |
| Delivery Cost          | delivery_cost          | DecimalField    | max_digits=6, decimal_places=2, null=False, default=0                                |
| Order Total            | order_total            | DecimalField    | max_digits=10, decimal_places=2, null=False, default=0                               |
| Final Total            | final_total            | DecimalField    | max_digits=10, decimal_places=2, null=False, default=0                               |
| Orignal Trolley        | original_trolley       | TextField       | null=False, blank=False, default=''                                                  |
| Stripe PID             | stripe_pid             | CharField       | max_length=254, null=False, blank=False, default=''                                  |
|                        |                        |                 |                                                                                      |

## Order Lineitems model
| Name               | Database Key       | Field Type     | Validation                                                                         |
|--------------------|--------------------|----------------|------------------------------------------------------------------------------------|
| ------------------ | ------------------ | -------------- | ------------                                                                       |
| Order              | order              | ForeignKey     | Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems' |
| Product            | product            | ForeignKey     | Product, null=False, blank=False, on_delete=models.CASCADE                         |
| Product Size       | product_size       | CharField      | max_length=4, null=True, blank=True                                                |
| Product Quantity   | quantity           | IntegerField   | null=False, blank=False, default=0                                                 |
| Lineitem Total     | lineitem_total     | DecimalField   | max_digits=6, decimal_places=2, null=False, blank=False, editable=False            |
|                    |                    |                |                                                                                    |

## Entity Relationship Diagram
![Image of ERD DB Diagram](writeup_files/images/erd.png)