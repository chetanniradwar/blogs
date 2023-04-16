
## Project Setup for Mac

1. install brew using `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2. install pipenv globally using `brew install pipenv`

3. install postgres using `brew install postgres`

4. On terminal `createuser -s postgres
psql -U postgres` to create 'postgres' user with password 'postgres' and login to psql via postgress user`

5. if psql terminal not opened then on terminal write `psql` to open postgres command terminal

6. switch to postgres user if user is not postgres by `psql -U postgres`

7. on psql `CREATE DATABASE blogs;` to create blogs database

8. create a project folder `blogs`

9. clone the git repo locally using `git clone https://github.com/chetanniradwar/blogs.git` in 'blogs' folder

10. in current folder run `pipenv shell` to create virtual environment

11. `pipenv install` to install all the project dependencies

12. then, `cd blog_platform` folder inside which `manage.py` file is there.

13. run `python manage.py migrate` to migrate all migrations and create table in the database

14. run `python manage.py runserver` to run the development server on 8000 port


## Postman documentation link
- [postman doc link](https://documenter.getpostman.com/view/20803750/2s93XyThu2)


## Technologies Used
- `djangorestframework` - to make REST apis in django
- `pipenv` - for making virtual environment
- `requests` - to make https requests using python
- `json` - to convert json to python dictionary and vice versa
- `pytest` - for writing unit test cases
