# Practical Bug Bounty

Welcome to the Practical Bug Bounty project! This platform is designed to help users discover bug bounty-related videos, organized into categories, offering a curriculum-like experience.



https://github.com/PatrikFehrenbach/practical-bug-bounty/assets/9072595/5a3d0f39-f3d0-437f-8d01-3c59e07b2eb4




## 🚧 Project Status: In Development 🚧

This project is currently in its development phase and there's a lot more to be done. I am actively seeking community contributions to make this platform even better!

<!-- ### Demo Credentials
For those who want to check out the current state of the project, we have set up a demo account:

Go to http://localhost:8000/admin

- **Username:** `test`
- **Password:** `test`

However, please note that this is a development version, and it's highly recommended to not use these credentials for production. --> 

## Features

- **Video Organization:** Discover the latest bug bounty videos, neatly organized into various categories.
- **Course Curriculum:** Provides a curriculum-like structure for streamlined learning.
- **Community Driven:** Built with love by the community, for the community.

## Contributing

I am always welcoming contributions from everyone! Whether it's a typo fix, a new feature, or a bug fix, your help is greatly appreciated. 

## Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/patrikfehrenbach/practical-bug-bounty.git practical-bug-bounty/
   cd practical-bug-bounty
   ```

2. **Install Django + Addons**
    ```bash
    python3 -m pip install -r requirements.txt
    ```

3. **Run migrations**
    ```bash
    cd bugbountytube/
    python3 manage.py migrate
    ```

4. **Create super user**
    ```bash
    python3 manage.py createsuperuser
    ```

5. **Run the server**
    ```bash
    python3 manage.py runserver
    ```

6. **Navigate to http://localhost:8000**

## Usage

### To Create a new Module: 

1. Log into the Backend http://localhost:8000/admin
2. Go to Categories -> Click on add
3. Fill in the details
4. Click on Save
<img width="1234" alt="Screenshot 2023-10-06 at 12 49 53" src="https://github.com/PatrikFehrenbach/practical-bug-bounty/assets/9072595/fca93d4c-efce-4e7b-b5ca-dac3e4d13a55">

### To Link a Video to a Module 

1. Log into the Backend http://localhost:8000/admin
2. Go to Videos -> Click on add
3. Fill in the details
4. Click on Save 

<img width="904" alt="Screenshot 2023-10-06 at 12 50 27" src="https://github.com/PatrikFehrenbach/practical-bug-bounty/assets/9072595/b13459bc-4788-4ea4-a3a8-3a918fe820a1">


Made with ❤️ by @itsecurityguard for the Open Source community.

