"""Command that fills the database with demo data: python manage.py seed_demo"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from contact.models import ContactInfo
from main.models import Establishment, Testimonial
from menu.models import Category, Dish
from service.models import Service
from team.models import Chef


def copy_image(source_name, folder):
    """Copies an image from static/images into media/<folder> and returns the model path."""
    source = Path(settings.BASE_DIR) / "static" / "images" / source_name
    if not source.exists():
        return ""
    target_dir = Path(settings.MEDIA_ROOT) / folder
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, target_dir / source_name)
    return "%s/%s" % (folder, source_name)


class Command(BaseCommand):
    help = "Fills the database with demo data for every section of the site"

    def handle(self, *args, **options):
        Establishment.objects.all().delete()
        Testimonial.objects.all().delete()
        Category.objects.all().delete()
        Chef.objects.all().delete()
        Service.objects.all().delete()
        ContactInfo.objects.all().delete()

        Establishment.objects.create(
            name="CakeZone",
            slogan="Handmade cakes for your celebrations",
            short_description="CakeZone bakery - custom cakes made of natural ingredients.",
            description=(
                "We have been baking cakes since 2010: birthdays, weddings and corporate parties. "
                "Every cake is made by hand from fresh products following your own sketch."
            ),
            image=copy_image("about.jpg", "establishment"),
            years_of_experience=15,
            cakes_baked=8400,
            happy_clients=5200,
            master_chefs=6,
            awards=12,
        )

        testimonials = [
            ("Mary Brown", "designer",
             "I ordered a wedding cake, the guests loved it, the taste is amazing.",
             5, "testimonial-1.jpg"),
            ("Oleg Wilson", "manager",
             "They made a birthday cake for my daughter quickly and right on time.",
             5, "testimonial-2.jpg"),
            ("Anna Clark", "doctor",
             "Beautiful decoration and an honest list of ingredients. I will order again.",
             4, "testimonial-3.jpg"),
            ("Dmitry Walker", "developer",
             "We ordered a cake for a corporate party, the colleagues appreciated it.",
             5, "testimonial-4.jpg"),
        ]
        for name, profession, text, rating, photo in testimonials:
            Testimonial.objects.create(
                author_name=name, profession=profession, text=text,
                rating=rating, photo=copy_image(photo, "testimonials"),
            )

        categories = [
            ("Birthday", "birthday", "Birthday cakes", 1),
            ("Wedding", "wedding", "Wedding cakes", 2),
            ("Custom", "custom", "Cakes made from your own sketch", 3),
        ]
        dishes = {
            "birthday": [
                ("Chocolate cake", "Sponge cake with chocolate ganache",
                 850, 1500, "cake-1.jpg"),
                ("Red Velvet cake", "A classic one with cream cheese",
                 990, 1600, "cake-2.jpg"),
                ("Kids cake", "Bright decoration and milk cream",
                 780, 1400, "cake-3.jpg"),
            ],
            "wedding": [
                ("Two-tier wedding cake", "Vanilla sponge cake with berries",
                 2400, 4000, "cake-2.jpg"),
                ("Naked wedding cake", "No fondant, with fresh flowers",
                 2100, 3500, "cake-1.jpg"),
            ],
            "custom": [
                ("Cake from a sketch", "Fully based on your own drawing",
                 1800, 3000, "cake-3.jpg"),
                ("Corporate cake", "With the company logo",
                 1600, 2800, "cake-1.jpg"),
            ],
        }
        for name, slug, description, order in categories:
            cat = Category.objects.create(
                name=name, slug=slug, description=description, order=order,
            )
            for dish_name, dish_description, price, weight, image in dishes[slug]:
                Dish.objects.create(
                    category=cat, name=dish_name, description=dish_description,
                    price=price, weight=weight, image=copy_image(image, "dishes"),
                )

        chefs = [
            ("John Smith", "head pastry chef", 10, "team-1.jpg",
             "Responsible for the signature recipes and the wedding cakes."),
            ("Mary Turner", "pastry chef", 6, "team-2.jpg",
             "Specialises in decoration and fondant work."),
            ("Oleg Fisher", "baker", 8, "team-3.jpg",
             "Bakes the sponge and shortcrust bases."),
        ]
        for index, chef in enumerate(chefs, start=1):
            full_name, designation, years, photo, biography = chef
            Chef.objects.create(
                full_name=full_name, designation=designation, experience_years=years,
                biography=biography, photo=copy_image(photo, "chefs"), order=index,
                facebook="https://facebook.com/", twitter="https://twitter.com/",
                linkedin="https://linkedin.com/",
            )

        services = [
            ("Birthday cakes",
             "We bake a cake of the size and decoration you need for your party.",
             "bi bi-gift", 780, 1),
            ("Wedding cakes",
             "Multi-tier cakes and a tasting before the order.",
             "bi bi-heart", 2100, 2),
            ("Cakes from a sketch",
             "We bring any drawing or idea of yours to life.",
             "bi bi-brush", 1600, 3),
        ]
        for title, description, icon, price, order in services:
            Service.objects.create(
                title=title, description=description, icon=icon,
                price_from=price, order=order,
            )

        ContactInfo.objects.create(
            office_address="12 Khreshchatyk Street, Kyiv",
            email="info@cakezone.example",
            phone="+38 (067) 123-45-67",
            working_hours_weekdays="09:00 - 19:00",
            working_hours_weekend="10:00 - 17:00",
            facebook="https://facebook.com/",
            instagram="https://instagram.com/",
            twitter="https://twitter.com/",
        )

        self.stdout.write(self.style.SUCCESS("Demo data has been added."))
