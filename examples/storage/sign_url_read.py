# [START import]
from nitric.api import Storage
from nitric.api.storage import FileMode

# [END import]
async def storage_sign_url_read():
    # [START snippet]
    # Construct a new storage client with default settings
    storage = Storage()

    # Create a readonly presigned url for the file valid for the next 3600 seconds
    await storage.bucket("my-bucket").file("path/to/item").sign_url(mode=FileMode.READ, expiry=3600)


# [END snippet]
