from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from storages.backends.azure_storage import AzureStorage
import os

class StaticFileStorage(S3Boto3Storage):
  location = settings.STATICFILES_FOLDER

class MediaFileStorage(S3Boto3Storage):
  location = settings.MEDIAFILES_FOLDER

class AzureMediaStorage(AzureStorage):
    account_name = os.getenv("AZURE_ACCOUNT_NAME")
    account_key = os.getenv("AZURE_ACCOUNT_KEY")
    azure_container = os.getenv("AZURE_CONTAINER")
    expiration_secs = None