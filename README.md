# CS551Q_Solo_App_Final
For guests, they can buy time. If they become users, they can buy and sell time. 
There are admin tools to see purchases and activity. Faker used to create some 
users. 

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

## Render
username: seluvaiasariahita@gmail.com
paswrd: secret1234!
https://cs551q-solo-app-final.onrender.com


## Admin Panel
Log in at http://localhost:8000/admin
- username = "username"
- email = "user@example.com"
- temp_pswrd = "secret123!"

## Notes
- possible to change to PostgreSQL but codio hasn't worked well with it when I've done it in the past
- functions in views that don't connect to html because they're just to show the potential of the direction 
    but didn't want to connect just yet to html