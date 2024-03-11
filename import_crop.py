# create_model_instances.py
import os
import django
import csv

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fasal_saathi.settings')  # Replace 'yourproject.settings' with your actual settings module

# Initialize Django
django.setup()

from app.models import Crop

def import_data_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            Crop.objects.create(
                crop_image=row['crop_image'],
                season=row['season'],
                name=row['name'],
                type=row['type'],
                month_of_harvest=row['month_of_harvest'],
                medicines_pesticides=row['medicines_pesticides'],
                soil=row['soil']
            )

if __name__ == "__main__":
    csv_file_path = "data/FasalSaathi_crop_type.csv"
    import_data_from_csv(csv_file_path)
