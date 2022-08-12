# Receipts
This project is created on **Django** framework. 

In this website the user can **register, login** and by doing so, gets access to the data that is displayed. The data is
table of _users_, who can add a _receipt_ to the table, and the table of the _receipts_, which _users_ can reorder based on their 
personal _preference_ or add a new one. ****All of the data** is available to **all users**, but its order is **unique for each user****. 

In case you need to edit some receipt you must ask the "_staff_" member to **edit** or **delete** it. 

When the user has reordered something in the table of the receipts, the information of his new preference is
passed to the backend, where it is stored in the **PostgreSQl** database. The actual drag and drop reordering is implemented
on the front-end via **SortableJS**. So, when we change the indexing of items in list we pass that data to the backend ,
where it updates the order. **All actions regarding changes in the table of receipts are dynamic,** meaning you do not have to refresh
the page to view something. 


**_Here is the DemoVideo of the functionality of the website on GoogleDrive:_**
https://drive.google.com/file/d/1sJkL-6oV0ac6CST4CgaZm1nKLfHdbccq/view?usp=sharing

If you wish to install the project and run locally, please follow this steps:

```
1. git clone https://github.com/NazarGorynych/receipts.git
2. pip install virtualenv
3. virtualenv env
4. source env/bin/active
5. pip install -r requirements.txt

6. create PostgreSQL database locally and connect it in settings
7. generate new SECRET_KEY (python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
 and change it in settings 
9. python manage.py makemigrations
10. python manage.py migrate

11. python manage.py runserver
```
**WARNING!** you can not use SQLite3 instead of Postgres due to ArrayField in OrderingPreference model.

(C) 2022 Nazarii Horchytsia, Khmelnytskyi, Ukraine
Email: nazarii.horchytsia@gmail.com
