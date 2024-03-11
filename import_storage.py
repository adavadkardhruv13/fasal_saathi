# create_model_instances.py
import os
import django
import csv

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fasal_saathi.settings')  # Replace 'fasal_saathi.settings' with your actual settings module

# Initialize Django
django.setup()

# Rest of your script
from app.models import StorageSpace

def import_data_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            StorageSpace.objects.create(
                name=row['name'],
                location=row['location'],
                capacity=float(row['capacity']),
                available=row['available'],
                available_from=row['available_from'],
                availability_duration=int(row['availability_duration']),
                contact=int(row['contact']),
                storage_type=row['storage_type'],
                storage_image=row['storage_image'],  # Assuming the CSV has a column named 'storage_image' with file paths
                price=int(row['price'])
            )

if __name__ == "__main__":
    csv_file_path = "data/FasalSaathi-storage.csv"
    import_data_from_csv(csv_file_path)
