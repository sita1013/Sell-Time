# CS551Q_Solo_App_Final
solo app focused on selling time


Directions on seeding in the data
# After running migrations
python manage.py shell
>>> from yourapp.models import TimePackage
>>> TimePackage.seed_packages()