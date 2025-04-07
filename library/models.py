from django.db import models

# Create your models here.
class LibraryItem:
    def __init__(self, id, title, category, photo, period, cost, url):
        self.id = id
        self.title = title
        self.category = category
        self.photo = photo
        self.period = period
        self.cost = cost
        self.url = url

item1 = LibraryItem(
    1,
    "Lawn Aerator",
    "Lawn",
    "img/aerator.png",
    "3-day rental",
    80,
    "item.html"
)

item2 = LibraryItem(
    2,
    "Lawn Mower",
    "Lawn",
    "img/mower.png",
    "2-day rental",
    15,
    "item.html"
)

item3 = LibraryItem(
    3,
    "Seeder",
    "Lawn",
    "img/seeder.png",
    "3-day rental",
    15,
    "item.html"
)

item4 = LibraryItem(
    4,
    "Weed Eater",
    "Lawn",
    "img/weed-eater.png",
    "5-day rental",
    25,
    "item.html"
)

item5 = LibraryItem(
    5,
    "Rake",
    "Lawn",
    "img/rake.png",
    "5-day rental",
    5,
    "item.html"
)
# https://media.istockphoto.com/id/157256122/photo/fall-leaves-with-rake.jpg?s=612x612&w=0&k=20&c=xil-TwDn760PnJ9rFYbvCXVc5CRLkooQs3wdA5hNu6A=

item6 = LibraryItem(
    6,
    "Garden Toolset",
    "Lawn",
    "img/garden-set.png",
    "2-day rental",
    15,
    "item.html"
)
# https://t3.ftcdn.net/jpg/03/23/16/24/360_F_323162416_Qf6AALct1iUycjPm1VVrqZ0GpfepsBt9.jpg

item7 = LibraryItem(
    7,
    "Shredder",
    "Lawn",
    "img/shredder.png",
    "2-day rental",
    50,
    "item.html"
)
# https://media.istockphoto.com/id/1519392687/photo/plant-shredder-close-to-a-wheelbarrow-filled-with-mulch-in-a-lawn.jpg?s=612x612&w=0&k=20&c=SczUUgwiYRwmEKBOkrtX6DKNJIjNFBI_phPRBw1jnkU=

# These items hold the "featured" homepage items
item8 = LibraryItem(
    8,
    "Wingspan Board Game",
    "Games",
    "img/wingspan.png",
    "3-day rental",
    5,
    "item.html"
)

item9 = LibraryItem(
    9,
    "The Office BluRay",
    "TV Shows",
    "img/office.png",
    "7-day rental",
    5,
    "item.html"
)

library_items = []
library_items.append(item1)
library_items.append(item2)
library_items.append(item3)
library_items.append(item4)
library_items.append(item5)
library_items.append(item6)
library_items.append(item7)
library_items.append(item8)
library_items.append(item9)


regular_user = {"username": "rick", "password": "regular"}
admin_user = {"username": "andy", "password": "admin"}