# Heroku Deployment

1. I went to heroku logged in and created an app with a unique name for my project.

1. Once the app was created, I then click on resources tab and installed heroku postgres and choose hobby dev free option.

1. Then I went to my VSCode and install the following packages using the following commands in the terminal:

    `pip3 install dj_database_url`

    `pip3 install psycopg2-binary`

1. Then i froze the requirements using the following command in the terminal:

    `pip3 freeze --local > requirements.txt`

1. Then I went to the settings.py file in the main project app dir and put at the top under import os the line of code:

    `import dj_database_url`

1. Then scrolled down to the database section in the settings.py and commented out the default database config and added this block of code.
    ```
    DATABASES = {
        'default': dj_database_url.parse('mypostgresurl')
    }
    ```
1. To get the postgres url, I had to go to my heroku project settings tab and then I clicked on the reveal config vars button and copied postgres URL address.

1. Now I needed to do a migrate to the new postgres database, but before running a full migration I ran this command in the terminal:

    `python3 manage.py showmigrations`


    To see which models were going to be migrated to the new database. 

1. Once checked I then run the following command to migrate the models to the new database:
    `python3 manage.py migrate`

1. Nows I had to populate the database by loading the categories and product fixture to it. An important note here to load  the categories fixture first then products fixture because the products rely on the categories data. I ran the following command in the terminal to load the fixtures:

    `python3 manage.py loaddata categories`

    `python3 manage.py loaddata products`

1. Now a superuser needed to be created and to do this I ran the following command in the terminal:

    `python3 manage.py createsuperuser`

    ```
    Username: ausername
    Email: aemailaddress@email.com
    Password: apassword
    Password Confirm: apassword
    ```

1. The next thing to do is start to setup the working environment to properly deploy to heroku, for the database section I addws this block of code.
    ```
    if 'DATABASE_URL' in os.environ:
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
    ```

1. Now I installed the webserver called gunicorn using this command in the terminal:

    `pip3 install gunicorn`

1. After freezing the requirements, I then created the a Procfile in the main directory and added this line of code with no whitespaces at the end and now new line underneath within the Procfile.

    `web: gunicorn ur_gym.wsgi:application`

1. I then to install heroku for the next part and I used the following command:

    `curl https://cli-assets.heroku.com/install.sh | sh`

1. Then I needed to login into heroku using the terminal, so i typed in the following command:

    `heroku login`

1. Once logged in I needed to temporarily disable collectstatic using this heroku command

    `heroku config:set DISABLE_COLLECTSTATIC=1 --app iftikhan-ms4-project-urgym`

1. Then I scrolled up the main settings.py file to the allowed host section and added this url within the square bracket. 
ALLOWED_HOSTS = ['iftikhan-ms4-project-urgym.herokuapp.com', 'localhost']

1. I then started modify the settings.py file and added these if statements
    ```
    if 'SECRET_KEY' in os.environ:
        # Deployed env secret key
        SECRET_KEY = os.getenv("SECRET_KEY")
    else:
        # Development env secret key
        SECRET_KEY = myenv('SECRET_KEY')

    # Stripe ifs to check wether keys are in deployment or development
    if 'STRIPE_PUBLIC_KEY' in os.environ:
        STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", '')
    else:
        STRIPE_PUBLIC_KEY = myenv("STRIPE_PUBLIC_KEY")

    if 'STRIPE_SECRET_KEY' in os.environ:
        STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", '')
    else:
        STRIPE_SECRET_KEY = myenv("STRIPE_SECRET_KEY")

    if 'STRIPE_WH_SECRET' in os.environ:
        STRIPE_WH_SECRET = os.getenv("STRIPE_WH_SECRET", '')
    else:
        STRIPE_WH_SECRET = myenv("STRIPE_WH_SECRET")
    ```

1. Then I committed the change to GitHub, once that is done it is time to deploy to heroku,  by typing the following commands in the terminal:

    * First initialise the heroku remote, the name needs to be the same as the Heroku app name.
    `heroku git:remote -a iftikhan-ms4-project-urgym`

    * Then push to heroku using this command

    `git push heroku main`

### AWS deployment

This section here I followed the videos that the code institute provided, since this was new to me and I wanted to get it correct and make no errors

- Go on `aws.amazon.com` to create an AWS account.
- Once all the details have been filled out and you have created an account, you would need to go back to `aws.amazon.com` 
- Under my account, click on 'AWS Management Console'
- Search for s3 and once selected, create a new bucket that will store the files.
- Give the bucket a name and choose the location nearest to you
- Uncheck 'Block all public access' and acknowledge that the bucket would be made public.
- Once done, click on 'Create bucket'
- On the properties tab, turn on 'Static website hosting'
- for the index and error document, file it in with the suggested default values. Then click 'Save'
- In the permission tab, click on 'CORS configuration' and paste the following values as this will be required access between Heroku and the s3 bucket
    ```
    [
    {
        "AllowedHeaders": [
            "Authorization"
        ],
        "AllowedMethods": [
            "GET"
        ],
        "AllowedOrigins": [
            "*"
        ],
        "ExposeHeaders": []
    }
    ]
    ```
- Go to the policy tab and select policy generator so we can create a security policy for this bucket.
    - The policy type is going to be s3 bucket policy
    - Allow all principles by using a * 
    - Action will be, 'Get object'
    - Add the ARN (Amazon Resource Name)
    - Click 'Add Statement', then 'Generate Policy'
    - Copy the policy in the bucket policy editor 
    - Add a `/*` at the end of the resource key
    - Click Save
- Go to `Access Control List` and under the `Public Access` section, and select `List Objects` for everyone
- In the services menu, open `IAM`
- Create a group, and give it a name. Keeping clicking next till the group is created
- Click on policies from the side panel, and then create policy.
- Go to the JSON tab and then select import managed policy.
    - Search for `s3` and then choose `full access to s3`
    - In the JSON file where it says "Resources", after the semicolon, add the ARN. `[enterARN]`,`[enter it again with /*]`
    - Click on review policy and give it a name and a description and then 'Create Policy'.
- Click on 'Groups', click on the group that you created. Click on 'Attach Policy', search for your policy that was just created and select it.
- Click on 'User' to attach to the group from the left-hand side of the menu bar.
    - Click on 'Add user', give it a name, give them 'Programmatic access'.
    - Put them in a group we just created which has the policy attached to it.
    - Click next to the end till you create the user.
    - Download the CSV as that would give you the user access key and the secret access key which would need to authenticate the Jango app


21. Now that the S3 bucket is created and all the other things, now its time to connect django to S3. To do this two new packages need to be installed. 
`pip3 install boto3`
`pip3 install django-storages`

* Then I ran the freeze command into the requirements

* Also add storages to the main settings.py in the app section like this.
'storages',

22. Now in the we will connect django to s3 enter the following code in the main settings.py file under the static file section but before the stripe section.
    ```
    if 'USE_AWS' in os.environ:
        # S3 Bucket Config
        AWS_STORAGE_BUCKET_NAME = 'iftikhan-ms4-project-urgym'
        AWS_S3_REGION_NAME = 'eu-west-2'
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    ```
23. Then I went and added the aws secret key to the config vars
AWS_ACCESS_KEY_ID = accesskey
AWS_SECRET_ACCESS_KEY = secrectkey
USE_AWS = True

* And remove the the disable collection static var:
DISABLE_COLLECTSTATIC = 1

24. Now I need to create a custom file called: custom_storages.py to tell django in production to use S3 to store the uploaded product images. in the custom_storages.py file copy and paste this code.

    ```
    from django.conf import settings
    from storages.backends.s3boto3 import S3Boto3Storage


    class StaticStorage(S3Boto3Storage):
        location = settings.STATICFILES_LOCATION


    class MediaStorage(S3Boto3Storage):
        location = settings.MEDIAFILES_LOCATION
    ```

25. Then I went back to the main setting.py file and enter this code that will tell heroku the location of the static and media files.

    ```
    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'
    ```

26. We also need to add this line of code to override and set the URLS for static and media files.

    ```
    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'
    ```

27. The next thing to do is add the static file cacheing, this is optional and this will tell the browser its ok to cache the static files for a long time. enter this code above the bucket config but below the if use_aws if statement.

    ```
    # Cache control
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }
    ```

28. Once This is all done, I deployed everything to github and you will see in the S3 management console and static file has show up containing all static files like css and js files.

29. Now I needed to sort out the media files and had to manually upload them to my s3 bucket.

30. Now you need to make sure the admin email is verified, by logging into the admin and verifying the email address

31. Now its time to add the new stripe webhook key that will be linked to the deployed site, so go to the stipe website and click on developers, then webhooks and then click the add endpoint button.

* Then add this heroku URL to the endpoint URL box.
https://iftikhan-ms4-project-urgym.herokuapp.com//checkout/wh/

* Then click on receive all events and then click on add endpoint

* Then I went to heroku and entered the new secret in the config vars for the STRIPE_WH_SECRET.

* I then went back to the stripe webpage and click on the send test webhook button located in the top right and send a test webhook. you should see a test success in the popup box.

These where the very long steps that I took to deploy my project ot heroku