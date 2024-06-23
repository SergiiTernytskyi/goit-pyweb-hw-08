from models import Author, Quote
import redis
from redis_lru import RedisLRU

import connect


client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_author_name(name: str):
    print(f"Find quotes by author name {name}")

    authors = Author.objects(fullname__iregex=f"^{name}")
    result = {}
    for author in authors:
        quotes = Quote.objects(author=author)
        result[author.fullname] = [item.quote for item in quotes]
    return result


@cache
def find_by_tag(tag: str):
    print(f"Find quotes by {tag}")
    quotes = Quote.objects(tags__iregex=f"^{tag}")
    result = [q.quote for q in quotes]
    return result


def find_by_tags(tags: str):
    print(f"Find quotes by {tags}")
    tags_list = tags.split(",")
    quotes = Quote.objects(tags__in=tags_list)
    result = [q.quote for q in quotes]
    return result


def main():
    print(f"Welcome to the database assistant bot!")

    while True:
        user_input = input(f"Please enter desired command: ")
        try:
            cmd, *args = user_input.strip().lower().split(": ")
        except KeyError:
            return f"Oops! Try again, enter existing command name."
        except IndexError:
            return "Oops! Try again, enter the valid argument."

        if cmd == "exit":
            print(f"Good bye!")
            break
        elif cmd == "name":
            print(find_by_author_name(args[0]))
        elif cmd == "tag":
            print(find_by_tag(args[0]))
        elif cmd == "tags":
            print(find_by_tags(args[0]))
        else:
            print(f"Invalid command. Try again...")


if __name__ == "__main__":
    main()
