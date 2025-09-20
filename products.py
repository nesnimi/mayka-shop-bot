# products.py
from aiogram.types import FSInputFile

PRODUCTS = {
    "Tommy Hilfiger": [
        {
            "name": "1. Сумка Tommy Hilfiger",
            "price": 3400,
            "description": "Размер: 20х16х4 см",
            "more_photos": "<a href='https://t.me/maykashop/19'>Ещё фото</a>",
            "image": FSInputFile("th1.jpg")
        },
        {
            "name": "2. Сумка Tommy Hilfiger",
            "price": 3400,
            "description": "Размер: 20х16х4 см",
            "more_photos": "<a href='https://t.me/maykashop/25'>Ещё фото</a>",
            "image": FSInputFile("th2.jpg")
        }
    ],
    "Hugo Boss": [
        {
            "name": "1. Сумка  Hugo Boss",
            "price": 3700,
            "description": "Размер: 20x25x6 см",
            "more_photos": "<a href='https://t.me/maykashop/58'>Ещё фото</a>",
            "image": FSInputFile("hb1.jpg")
        },
        {
            "name": "2. Сумка  Hugo Boss",
            "price": 3700,
            "description": "Размер:  20x25x6 см",
            "more_photos": "<a href='https://t.me/maykashop/65'>Ещё фото</a>",
            "image": FSInputFile("hb2.jpg")
        },
        {
            "name": "3. Сумка  Hugo Boss",
            "price": 3500,
            "description": "Размер: 20х22х3 см",
            "more_photos": "<a href='https://t.me/maykashop/72'>Ещё фото</a>",
            "image": FSInputFile("hb3.jpg")
        },
        {
            "name": "4. Сумка  Hugo Boss",
            "price": 3700,
            "description": "Размер: 16x20x5 cм",
            "more_photos": "<a href='https://t.me/maykashop/79'>Ещё фото</a>",
            "image": FSInputFile("hb4.jpg")
        }
    ],
     "Diesel": [
        {
            "name": "1. Сумка Diesel",
            "price": 3700,
            "description": "Размер: 19x23x5 см",
            "more_photos": "<a href='https://t.me/maykashop/86'>Ещё фото</a>",
            "image": FSInputFile("diesel1.jpg")
        }
     ],
     "Calvin Klein": [
        {
            "name": "1. Сумка Calvin Klein",
            "price": 3500,
            "description": "Размер: 20х22х3 см",
            "more_photos": "<a href='https://t.me/maykashop/114'>Ещё фото</a>",
            "image": FSInputFile("cc1.jpg")
        }
     ],
    "Burberry": [
        {
            "name": "1. Сумка Burberry",
            "price": 3500,
            "description": "Размер: 20х22х3 см",
            "more_photos": "<a href='https://t.me/maykashop/128'>Ещё фото</a>",
            "image": FSInputFile("burberry1.jpg")
        }
    ],
    "Dickies": [
        {
            "name": "1. Сумка Dickies",
            "price": 1700,
            "description": "Размер: 19x18x6 см",
            "more_photos": "<a href='https://t.me/maykashop/105'>Ещё фото</a>",
            "image": FSInputFile("dickies1.jpg")
        }
    ],
    "Guess": [
        {
            "name": "1. Сумка Guess",
            "price": 3400,
            "description": "Размер: 20x24x3 см",
            "more_photos": "<a href='https://t.me/maykashop/142'>Ещё фото</a>",
            "image": FSInputFile("g1.jpg")
        },
        {
            "name": "2. Сумка Guess",
            "price": 3400,
            "description": "Размер: 20x24x3 см",
            "more_photos": "<a href='https://t.me/maykashop/135'>Ещё фото</a>",
            "image": FSInputFile("g2.jpg")
        }
    ],
    "Lacoste": [
        {
            "name": "1. Сумка Lacoste",
            "price": 3800,
            "description": "Размер: 25х19х5 см",
            "more_photos": "<a href='https://t.me/maykashop/31'>Ещё фото</a>",
            "image": FSInputFile("lac1.jpg")
        },
        {
            "name": "2. Сумка Lacoste",
            "price": 3800,
            "description": "Размер: 25x19x5 см",
            "more_photos": "<a href='https://t.me/maykashop/37'>Ещё фото</a>",
            "image": FSInputFile("lac2.jpg")
        },
        {
            "name": "3. Сумка Lacoste",
            "price": 3800,
            "description": "Размер: 8х22х6 см",
            "more_photos": "<a href='https://t.me/maykashop/44'>Ещё фото</a>",
            "image": FSInputFile("lac3.jpg")
        },
        {
            "name": "4. Сумка Lacoste",
            "price": 3600,
            "description": "Размер: 8х22х4 см",
            "more_photos": "<a href='https://t.me/maykashop/51'>Ещё фото</a>",
            "image": FSInputFile("lac4.jpg")
        }
    ],
    "Nike": [
        {
            "name": "1. Cумка Nike",
            "price": 1700,
            "description": "Размер: 17x22x6 см",
            "more_photos": "<a href='https://t.me/maykashop/149'>Ещё фото</a>",
            "image": FSInputFile("nike1.jpg")
        },
        {
            "name": "2. Cумка Nike",
            "price": 1700,
            "description": "Размер: 17x21x4 см",
            "more_photos": "<a href='https://t.me/maykashop/158'>Ещё фото</a>",
            "image": FSInputFile("nike2.jpg")
        },
        {
            "name": "3. Cумка Nike",
            "price": 1700,
            "description": "Размер: 15x22x5 см",
            "more_photos": "<a href='https://t.me/maykashop/167'>Ещё фото</a>",
            "image": FSInputFile("nike3.jpg")
        }
    ],
    "Vans": [
        {
            "name": "1. Сумка Vans",
            "price": 1700,
            "description": "Размер: 15x18x4 см",
            "more_photos": "<a href='https://t.me/maykashop/176?single'>Ещё фото</a>",
            "image": FSInputFile("vans1.jpg")
        }
    ]
}