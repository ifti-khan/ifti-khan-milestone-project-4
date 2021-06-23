# User Model
The User model I am using has come from the default Django authentication model and has been used by importing it from django.contrib.auth. For more information about Djangos authentication [click here](https://docs.djangoproject.com/en/3.2/ref/contrib/auth/) to find out more.

# Profile App
## Profile Model
| Name           | Database Key            | Field Type    | Validation |
|----------------|-------------------------|---------------|------------|
| User           | user                    | OneToOneField |            |
| Full Name      | profile_fullname        | CharField     |            |
| Contact Number | profile_contactnumber   | CharField     |            |
| Address Line 1 | profile_addressline1    | CharField     |            |
| Address Line 2 | profile_addressline2    | CharField     |            |
| Town / City    | profile_town_or_city    | CharField     |            |
| County / State | profile_county_or_state | CharField     |            |
| Postcode       | profile_postcode        | CharField     |            |
| Country        | profile_country         | CountryField  |            |
|                |                         |               |            |

## Category Model
| Name           | Database Key            | Field Type    | Validation |
|----------------|-------------------------|---------------|------------|
| Category Name  | category_name           | CharField     |            |
|                |                         |               |            |

# Product App
## Products Model
| Name                | Database Key        | Field Type   | Validation |
|---------------------|---------------------|--------------|------------|
| Category            | category            | ForeignKey   |            |
| Product Name        | product_name        | CharField    |            |
| Product Description | product_description | TextField    |            |
| Product Price       | product_price       | DecimalField |            |
| Product Rating      | product_rating      | DecimalField |            |
| SKU                 | sku                 | CharField    |            |
| Product Size        | product_size        | BooleanField |            |
| Product Image       | product_image       | ImageField   |            |
| Product Image URL   | product_url         | URLField     |            |
|                     |                     |              |            |

## Review Model
| Name           | Database Key   | Field Type    | Validation |
|----------------|----------------|---------------|------------|
| User           | user           | ForeignKey    |            |
| Review Title   | review_title   | CharField     |            |
| Review Rating  | review_rating  | IntegerField  |            |
| Review Content | review_content | TextField     |            |
| Review Date    | review_date    | DateTimeField |            |
| Review Time    | review_time    | DateTimeField |            |
|                |                |               |            |

# Messageboard App
## User Message Model
| Name             | Database Key     | Field Type    | Validation |
|------------------|------------------|---------------|------------|
| User             | user             | ForeignKey    |            |
| Message Category | message_category | CharField     |            |
| Message Replies  | message_replies  | IntegerField  |            |
| Message Date     | message_date     | DateTimeField |            |
| Message Time     | message_time     | DateTimeField |            |
| Message Title    | message_title    | CharField     |            |
| Message Content  | message_content  | TextField     |            |
|                  |                  |               |            |

## User Reply Model
| Name          | Database Key  | Field Type    | Validation |
|---------------|---------------|---------------|------------|
| User          | user          | ForeignKey    |            |
| Reply Content | reply_content | TextField     |            |
| Reply Date    | reply_date    | DateTimeField |            |
| Reply Time    | reply_time    | DateTimeField |            |
|               |               |               |            |

# Checkput App
## Orders
| Name                 | Database Key         | Field Type    | Validation |
|----------------------|----------------------|---------------|------------|
| Order Number         | order_number         | CharField     |            |
| User Profile         | user_profile         | ForeignKey    |            |
| Full Name            | full_name            | CharField     |            |
| Email                | email                | EmailField    |            |
| Contact Number       | contact_number       | CharField     |            |
| Address Line 1       | address_line1        | CharField     |            |
| Address Line 2       | address_line2        | CharField     |            |
| City / Town          | city_or_town         | CharField     |            |
| County / State       | county_state         | CharField     |            |
| Postcode             | postcode             | CharField     |            |
| Country              | country              | CountryField  |            |
| Order Date           | order_date           | DateTimeField |            |
| Delivery Cost        | delivery_cost        | DecimalField  |            |
| Order Total          | order_total          | DecimalField  |            |
| Final Total          | final_total          | DecimalField  |            |
| Original Trolley     | original_trolley     | TextField     |            |
| Stripe PID           | stripe_pid           | CharField     |            |
| Special Instructions | special_instructions | TextField     |            |
|                      |                      |               |            |

## Order Item Details
| Name             | Database Key     | Field Type   | Validation |
|------------------|------------------|--------------|------------|
| Order            | order            | ForeignKey   |            |
| Product          | product          | ForeignKey   |            |
| Product Size     | product_size     | CharField    |            |
| Product Quantity | product_quantity | IntegerField |            |
| Item Total       | item_total       | DecimalField |            |
|                  |                  |              |            |