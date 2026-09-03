first_name = "ada"
last_name = "lovelace"
full_name = f"{first_name} {last_name}"
print(f"Hello, {full_name.title()}!")


bicycles = ["trek", "cannondale", "redline", "specialized"]
print(bicycles)

message = f"My first bicycle was a {bicycles[0].title()}."
print(message)

for bicycle in bicycles:
    print(f"I have a {bicycle.title()} bicycle.")

test = []

magicians = ["alice", "david", "carolina"]
for magician in magicians:
    print(magician.title())
    print(f"{magician.title()}, that was a great trick!")
    print(f"I can't wait to see your next trick, {magician.title()}.\n")


if magicians:
    print("We have some magicians!")
else:
    print("No magicians are available.")

tuple = (1, 2, 3)
print(tuple)

for number in tuple:
    print(number)

alien_0 = {"color": "green", "points": 5}
print(alien_0)
print(f"The alien is {alien_0['color']} and is worth {alien_0['points']} points.")

alien_0["color"] = "yellow"
alien_0["points"] = 10
print(alien_0)
print(f"The alien is now {alien_0['color']} and is worth {alien_0['points']} points.")


point_value = alien_0.get("points", "No point value assigned.")
print(point_value)

user_0 = {
    "username": "efermi",
    "first": "enrico",
    "last": "fermi",
}

for key, value in user_0.items():
    print(f"\nKey: {key}")
    print(f"Value: {value}")


class Car:
    """A simple attempt to represent a car."""

    def __init__(self, make, model, year):
        """Initialize attributes to describe a car."""
        self.make = make
        self.model = model
        self.year = year

    def get_descriptive_name(self):
        """Return a neatly formatted descriptive name."""
        long_name = f"{self.year} {self.make} {self.model}"
        return long_name.title()


my_new_car = Car("audi", "a4", 2024)
print(my_new_car.get_descriptive_name())
