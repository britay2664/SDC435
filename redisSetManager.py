# Name: Brian Taylor
# Date: October 5, 2026
# Assignment: 1.8 Performance Assessment
# Python Application Accessing a Key-Value Database
# Purpose: Use an interactive menu to perform CRUD operations
# on Redis sets using the redis-py library.

from datetime import datetime
import redis


def get_set_name():
    """Prompt until the user enters a nonempty set name."""
    while True:
        name = input("Enter the set name: ").strip()
        if name:
            return name
        print("The set name cannot be blank.")


def get_members():
    """Accept one or more members separated by commas."""
    while True:
        entries = input("Enter members separated by commas: ")
        members = [item.strip() for item in entries.split(",")
                   if item.strip()]
        if members:
            return members
        print("Enter at least one member.")


def show_members(database, name):
    """Display members in a consistent, readable order."""
    members = sorted(database.smembers(name))
    print(f"Members of {name}:")
    for member in members:
        print(f"  {member}")
    print(f"Total members: {len(members)}")


def main():
    # Connect to the local Redis server using lab database 3.
    database = redis.Redis(
        host="127.0.0.1",
        port=6379,
        db=3,
        decode_responses=True
    )

    try:
        database.ping()
    except redis.RedisError as error:
        print(f"Could not connect to Redis: {error}")
        return

    print("Connected to Redis application database 3.")

    # Display the menu repeatedly and accept the user's choice.
    while True:
        print("\nRedis Set Manager")
        print("System date and time:",
              datetime.now().astimezone().isoformat(
                  sep=" ", timespec="seconds"
              ))
        print("1. Create a set")
        print("2. View a set")
        print("3. Update a set")
        print("4. Delete a set")
        print("5. Delete all data in application database 3")
        print("0. Exit")

        choice = input("Select an option: ").strip()

        try:
            # CREATE: Create a new set using user-provided members.
            if choice == "1":
                name = get_set_name()

                if database.exists(name):
                    print("That key already exists. Use another name.")
                    continue

                members = get_members()
                added = database.sadd(name, *members)
                print(f"Created '{name}' with {added} unique members.")

            # READ: Retrieve and display a specific set.
            elif choice == "2":
                name = get_set_name()

                if database.type(name) != "set":
                    print("That key does not exist or is not a set.")
                    continue

                show_members(database, name)

            # UPDATE: Add or remove members of an existing set.
            elif choice == "3":
                name = get_set_name()

                if database.type(name) != "set":
                    print("That key does not exist or is not a set.")
                    continue

                action = input(
                    "Enter A to add members or R to remove members: "
                ).strip().upper()

                if action not in ("A", "R"):
                    print("Invalid update option.")
                    continue

                members = get_members()

                if action == "A":
                    count = database.sadd(name, *members)
                    print(f"Added {count} new members.")
                else:
                    count = database.srem(name, *members)
                    print(f"Removed {count} members.")

                if database.exists(name):
                    show_members(database, name)
                else:
                    print("The last member was removed; the set is gone.")

            # DELETE: Delete one specific set.
            elif choice == "4":
                name = get_set_name()

                if database.type(name) != "set":
                    print("That key does not exist or is not a set.")
                    continue

                database.delete(name)
                print(f"Deleted set '{name}'.")
                print(f"Key exists after deletion: {database.exists(name)}")

            # DELETE ALL: Clear only the selected application database.
            elif choice == "5":
                confirmation = input(
                    "Type YES to delete all data in database 3: "
                ).strip()

                if confirmation == "YES":
                    database.flushdb()
                    print("All data in application database 3 deleted.")
                    print(f"Remaining keys: {database.dbsize()}")
                else:
                    print("Deletion canceled.")

            # Exit the application and close its Redis connection.
            elif choice == "0":
                database.close()
                print("Redis connection closed. Program ended.")
                print("System date and time:",
                      datetime.now().astimezone().isoformat(
                          sep=" ", timespec="seconds"
                      ))
                break

            else:
                print("Invalid selection. Choose 0 through 5.")

        except redis.RedisError as error:
            print(f"Redis operation failed: {error}")


if __name__ == "__main__":
    main()