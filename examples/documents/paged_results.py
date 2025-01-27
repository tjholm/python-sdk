# [START import]
from nitric.api import Documents

# [END import]
async def documents_paged_results():
    # [START snippet]
    docs = Documents()

    query = docs.collection("Customers").query().where("active", "==", True).limit(100)

    # Fetch first page
    results = await query.fetch()

    # Fetch next page
    if results.paging_token:
        results = await query.page_from(results.paging_token).fetch()


# [END snippet]
