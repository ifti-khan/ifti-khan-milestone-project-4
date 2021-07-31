To make a local clone you are going to need a few tool/software installed and setup a few things. 

## Tools/Software 
* An IDE like Gitpod or a Local Text Editor software like VSCode.
* The latest version of Python installed on your Local Machine if you are planning on using a Local Text Editor.

## Local Clone Steps
### Step 1 - Download
1. Open up your IDE or Local Text Editor, for demo purposes I am using VSCode. 

1. You need to make a clone of my repo and for this you need the repo address which can be found on my GitHub under the “Code” button 

    ![Local Clone](/writeup_files/screenshots/local-clone.jpg)

    Or the URL address below.

    ### My MS4 repo URL - https://github.com/ifti-khan/ifti-khan-milestone-project-4.git

1. Once you have the address, go to your VSCode and press the F1 key and type in clone, then you will see “Git: Clone”, click on that and then you will be prompted to enter the GitHub URL address located above. 

1. Copy and paste my repo URL and then press enter, you will then be prompted to find a save location for the repo.

1. Once you have a save location and have saved the repo and small popup will appear in the bottom right prompting you to open the project. 

1. Once you open the project, on the left you will see under the files tabs, my repo files and directories. 

### Step 2 - Environment Setup
1. Now that you have the file, you now need to install the project requirements from the requirements.txt file located in the main project directory.
    * To do this you need to type the following command In the terminal, `pip3 install -U -r requirements.txt`

1. Now its time to create and env file and this needs to go in the main project app directory called urgym.
    * THe file needs to be spelt exactly like this `.env`
1. Inside the `.env` file you will need to add the following variables for this project to work:
    ```
    SECRET_KEY=(yoursecretkeyhere)
    STRIPE_PUBLIC_KEY=(yourstripepublickeyhere)
    STRIPE_SECRET_KEY=(youryourstripesecretkeyherekeyhere)
    STRIPE_WH_SECRET=(yourstripewhsecretkeyhere)
    GMAPS_API=(yourgmapsapikeyhere)
    ```
1. Now the next thing that need to be done is to make migrations to the local database sqlite3
    * In the VSCode terminal type in the following command `python3 manage.py makemigrations --dry-run` this is to make sure that there are no errors before actually making a real migration

    * In the VSCode terminal type in the following command `python3 manage.py makemigrations`,

    * In the VSCode terminal type in the following command `python3 manage.py migrate --plan` this is to make sure that there are no errors before actually making a real migrate to the database

    * In the VSCode terminal type in the following command `python3 manage.py migrate`

1. Now that the migrations are done, it is time to populate the database by loading the following fixtures, the first fixture that need loading is the categories fixture.
    * In the VSCode terminal type in the following command `python3 manage.py loaddata categories`

1. The second and the last fixture to load to the database is the products fixture.
    * In the VSCode terminal type in the following command `python3 manage.py loaddata products`

1. Once all the fixtures are loaded it is time to create the superuser who is the admin to the web project and will be able to access the back end of the site.
    * In the VSCode terminal type in the following command `python3 manage.py createsuperuser`

1. Once the above command in entered there a few additional steps but these are personal steps and you need to write the key information down or make note of it.
    * You will need to type in a username.
    * Then an email address and make sure it is a valid email address.
    * A strong passwords
    * Lastly you need to confirm the password

1. Once this is all done, it is time to check and make sure the project can run on the server. To makes the project run on the development server you need to type in the following command into the VSCode terminal `python3 manage.py runserver`