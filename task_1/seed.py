import json
import connect

from models import Author, Quote


if __name__ == "__main__":
    with open("authors.json", encoding="utf-8") as file:
        data = json.load(file)
        for element in data:
            author = Author(
                fullname=element.get("fullname"),
                born_date=element.get("born_date"),
                born_location=element.get("born_location"),
                description=element.get("description"),
            )

            author.save()

    with open("quotes.json", encoding="utf-8") as file:
        data = json.load(file)
        for element in data:
            author, *_ = Author.objects(fullname=element.get("author"))
            quote = Quote(
                tags=element.get("tags"), quote=element.get("quote"), author=author
            )

            quote.save()
