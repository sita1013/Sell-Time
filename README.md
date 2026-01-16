# CS551Q_Solo_App_Final
For guests, they can buy time. If they become users, they can buy and sell time. 
There are admin tools to see purchases and activity. Faker used to create some 
users. 

# Note .env
No intention of making this a live application so .env having been committed and 
then made clear initially was a rookie mistake on my part. However, if people 
wanted to copy the code at all, please note that you should make sure the .env 
is embedded and you'll need to manage to make it private if you're planning to 
make it live for whatever reason. 

## Features
Buy Time: Select minutes for past or future use.
Sell Time: Authenticated users can list their time packages.
Cart Checkout: Secure session-based shopping cart.
User History: Track your purchase and sales history.
Guest Checkout: Purchase without signing up.
Admin Dashboard: View bar chart of weekly purchases.


## Directions for starting App
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_packages (creates both the time-packages and faker)
python3 manage.py shell
>>> from yourapp.models import TimePackage
>>> TimePackage.seed_packages()
python3 manage.py runserver 0.0.0.0:8000

- Go to localhost:8000

## Project Structure Highlights
sell_time/models.py – Core models (TimePackage, Purchase)
sell_time/views.py – Checkout logic, cart, user actions
sell_time/management/commands/seed_packages.py – Seeder with Faker
templates/ – All HTML pages (including admin customization)

## Notes
- possible to change to PostgreSQL but codio hasn't worked well with it when I've done it in the past
- functions in views that don't connect to html because they're just to show the potential of the direction 
    but didn't want to connect just yet to html
