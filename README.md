# CS551Q_Solo_App_Final
solo app focused on selling time



# Directions on seeding in the data // After running migrations
python3 manage.py shell
>>> from yourapp.models import TimePackage
>>> TimePackage.seed_packages()
python3 manage.py seed_timepackages


SuperUser:
username = username
email = user@example.com
pswrd = secret123!
