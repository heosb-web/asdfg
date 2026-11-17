
import requests


API_URL = "https://api.inaturalist.org/v1/taxa/autocomplete"


def search_species(keyword):

    if not keyword or not keyword.strip():
        return []

    params = {
        "q": keyword.strip(),
        "per_page": 100
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    results = []

    for item in data.get("results", []):

        scientific_name = item.get("name") or ""

        common_name = (
            item.get("preferred_common_name")
            or scientific_name
        )

        photo = item.get("default_photo") or {}

        species = {
            "inat_id": item.get("id"),
            "name": common_name,
            "scientific_name": scientific_name,
            "image_url": photo.get("medium_url")
        }

        results.append(species)

    return results
