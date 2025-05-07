# django-jobportal-webapp

## Live Website

Check out the live version of the website here: [Live Website](https://django-jobportal-webapp.onrender.com)

## Setup Instructions

Follow the steps below to set up the project locally.

### 1. **Clone the repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/DevPatel1479/django-jobportal-webapp.git
   cd django-jobportal-webapp

### 2. **Create and Activate the Virtual Environment**

      The project uses a virtual environment for dependencies. To set it up:

      Windows:
        python -m venv webvenv
        webvenv\Scripts\activate

      macOS/Linux:
        python3 -m venv webvenv
        source webvenv/bin/activate
    This will activate the virtual environment, and your terminal should show (webvenv) as the prompt.

### 3. **Install Dependencies**

      Once the virtual environment is activated, install the required dependencies listed in requirements.txt:
        pip install -r requirements.txt

### 4. **Setup Environment Variables**

      Create a .env file in the project root directory (if not already provided). You can copy the contents from .env.example (if it exists) or set the following environment       variables manually in the .env file:

           DATABASE_URL=postgres://user:password@localhost:5432/your_db
           EMAIL_HOST_USER=useremail@gmail.com
           EMAIL_HOST_PASSWORD=<password>

      Replace the actual values for the above config.


### 5. **Apply Database Migrations**

      Next, you'll need to apply the migrations to set up the database schema:
         python manage.py migrate
      This will create the necessary tables in your database.

### 6. **Run the Development Server**

      Finally, run the Django development server to start the application:
      python manage.py runserver

    The site should now be accessible at http://127.0.0.1:8000/ on your local machine.

### 7. Create super user

     To access the Django admin panel, you'll need to create a superuser account:
        python manage.py createsuperuser


        



  
    
