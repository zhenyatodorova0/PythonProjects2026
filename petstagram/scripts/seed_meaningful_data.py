import random
from datetime import date

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction

from common.models import Comment, Like
from pets.models import Pet
from photos.models import Photo

UserModel = get_user_model()

# 1x1 transparent PNG
PNG_BYTES = bytes.fromhex(
    "89504E470D0A1A0A0000000D49484452000000010000000108060000001F15C489"
    "0000000A49444154789C6360000002000154A24F5A0000000049454E44AE426082"
)

USERS = [
    {
        "username": "seed_emily",
        "email": "emily.petlover@example.com",
        "password": "pass1234",
        "first_name": "Emily",
        "last_name": "Carter",
    },
    {
        "username": "seed_daniel",
        "email": "daniel.trails@example.com",
        "password": "pass1234",
        "first_name": "Daniel",
        "last_name": "Meyer",
    },
    {
        "username": "seed_sophia",
        "email": "sophia.paws@example.com",
        "password": "pass1234",
        "first_name": "Sophia",
        "last_name": "Reed",
    },
]

PETS = [
    {
        "name": "Mochi",
        "owner": "seed_emily",
        "date_of_birth": date(2021, 5, 14),
        "personal_photo": "https://images.unsplash.com/photo-1517849845537-4d257902454a",
    },
    {
        "name": "Rex",
        "owner": "seed_daniel",
        "date_of_birth": date(2019, 8, 2),
        "personal_photo": "https://images.unsplash.com/photo-1507146426996-ef05306b995a",
    },
    {
        "name": "Nala",
        "owner": "seed_sophia",
        "date_of_birth": date(2020, 11, 30),
        "personal_photo": "https://images.unsplash.com/photo-1519052537078-e6302a4968d4",
    },
    {
        "name": "Kiwi",
        "owner": "seed_emily",
        "date_of_birth": date(2022, 3, 9),
        "personal_photo": "https://images.unsplash.com/photo-1548199973-03cce0bbc87b",
    },
    {
        "name": "Atlas",
        "owner": "seed_daniel",
        "date_of_birth": date(2018, 7, 21),
        "personal_photo": "https://images.unsplash.com/photo-1444212477490-ca407925329e",
    },
]

PHOTO_DESCRIPTIONS = [
    "Morning walk and a lot of zoomies in the park.",
    "Lazy Sunday afternoon nap by the window.",
    "Found the best hiking trail near the river today.",
    "Treat training session went better than expected.",
    "Golden hour portrait after a long play session.",
    "First beach visit and instant love for the sand.",
]

LOCATIONS = ["Sofia", "Plovdiv", "Varna", "Burgas", "Rila", "Vitosha"]

COMMENTS = [
    "This is such a great shot!",
    "Absolutely adorable.",
    "Looks like a perfect day outside.",
    "That expression is priceless.",
    "The lighting here is amazing.",
    "I can almost feel the happy energy.",
]


def create_or_update_users():
    users = {}
    for row in USERS:
        user, created = UserModel.objects.get_or_create(
            username=row["username"],
            defaults={
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
            },
        )
        if not created:
            user.email = row["email"]
            user.first_name = row["first_name"]
            user.last_name = row["last_name"]
        user.set_password(row["password"])
        user.save()
        users[row["username"]] = user
    return users


def recreate_seed_data(users):
    seed_users = list(users.values())

    # Remove previous seed objects (keeps script idempotent for quick reruns)
    Pet.objects.filter(user__in=seed_users).delete()

    pets = []
    for row in PETS:
        pet = Pet.objects.create(
            name=row["name"],
            user=users[row["owner"]],
            personal_photo=row["personal_photo"],
            date_of_birth=row["date_of_birth"],
        )
        pets.append(pet)

    photos = []
    for idx, description in enumerate(PHOTO_DESCRIPTIONS, start=1):
        photo = Photo.objects.create(
            description=description,
            location=random.choice(LOCATIONS),
        )
        photo.photo.save(
            f"seed_photo_{idx}.png",
            ContentFile(PNG_BYTES),
            save=True,
        )

        tagged = random.sample(pets, k=random.randint(1, min(3, len(pets))))
        photo.tagged_pets.set(tagged)
        photos.append(photo)

    for photo in photos:
        for _ in range(random.randint(2, 4)):
            Comment.objects.create(
                text=random.choice(COMMENTS),
                to_photo=photo,
            )

        Like.objects.bulk_create([
            Like(to_photo=photo) for _ in range(random.randint(3, 9))
        ])

    return {
        "users": len(seed_users),
        "pets": len(pets),
        "photos": len(photos),
        "comments": Comment.objects.filter(to_photo__in=photos).count(),
        "likes": Like.objects.filter(to_photo__in=photos).count(),
    }


@transaction.atomic
def main():
    users = create_or_update_users()
    stats = recreate_seed_data(users)

    print("Seed data created successfully:")
    for key, value in stats.items():
        print(f"- {key}: {value}")


main()
