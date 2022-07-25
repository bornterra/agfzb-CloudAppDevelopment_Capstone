from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object


class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='SampleMake')
    description = models.TextField(null=False, max_length=300, default='Sample description')
    
    def __str__(self):
        return self.name

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    make = models.ForeignKey('CarMake',on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30, default='SampleModel')
    dealerid = models.IntegerField()
    year = models.IntegerField()
    type_list = (
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Coupe', 'Coupe'),
    )

    modeltype = models.CharField(
        choices=type_list,
        blank=True,
        max_length=30
    )
    
    car_manager = models.Manager()
    
    def __str__(self):
        return f'{self.name},{self.make},{self.year}'

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
