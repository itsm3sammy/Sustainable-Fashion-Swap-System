import json
import os
from abc import ABC, abstractmethod

class ClothingItem(ABC):
    def __init__(self, title, item_id):
        self._title = title
        self._item_id = item_id

    @property
    def title(self):
        return self._title

    @property
    def item_id(self):
        return self._item_id

    @abstractmethod
    def display_details(self):
        pass

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "title": self.title,
            "item_id": self.item_id
        }

    @staticmethod
    def from_dict(data):
        if not isinstance(data, dict):
            return None
        if data["type"] == "Topwear":
            return Topwear(data["title"], data["item_id"], data["brand"], data["size"], data["color"])
        elif data["type"] == "Bottomwear":
            return Bottomwear(data["title"], data["item_id"], data["waist_size"], data["length"], data["material"])
        return None

class Topwear(ClothingItem):
    def __init__(self, title, item_id, brand, size, color):
        super().__init__(title, item_id)
        self.brand = brand
        self.size = size
        self.color = color

    def display_details(self):
        print(f"[Topwear] ID: {self.item_id}, Title: {self.title}, Brand: {self.brand}, Size: {self.size}, Color: {self.color}")

    def to_dict(self):
        base = super().to_dict()
        base.update({"brand": self.brand, "size": self.size, "color": self.color})
        return base

class Bottomwear(ClothingItem):
    def __init__(self, title, item_id, waist_size, length, material):
        super().__init__(title, item_id)
        self.waist_size = waist_size
        self.length = length
        self.material = material

    def display_details(self):
        print(f"[Bottomwear] ID: {self.item_id}, Title: {self.title}, Waist: {self.waist_size}, Length: {self.length}, Material: {self.material}")

    def to_dict(self):
        base = super().to_dict()
        base.update({"waist_size": self.waist_size, "length": self.length, "material": self.material})
        return base

class SwapMember:
    def __init__(self, member_id, name, password, borrowed_items=None):
        self._member_id = member_id
        self._name = name
        self._password = password
        self._borrowed_items = borrowed_items if borrowed_items else []

    def to_dict(self):
        return {
            "member_id": self._member_id,
            "name": self._name,
            "password": self._password,
            "borrowed_items": self._borrowed_items
        }

class SwapSystem:
    def __init__(self):
        self.items = {}      
        self.members = {}    
        self.load_data()

    def load_data(self):
        if os.path.exists("items.json"):
            with open("items.json", "r") as f:
                for item in json.load(f):
                    obj = ClothingItem.from_dict(item)
                    if obj:
                        self.items[obj.item_id] = obj

        if os.path.exists("users.json"):
            with open("users.json", "r") as f:
                for user in json.load(f):
                    self.members[user["member_id"]] = SwapMember(
                        user["member_id"],
                        user["name"],
                        user["password"],
                        user.get("borrowed_items", [])
                    )

    def save_data(self):
        with open("items.json", "w") as f:
            json.dump([item.to_dict() for item in self.items.values()], f, indent=4)

        with open("users.json", "w") as f:
            json.dump([member.to_dict() for member in self.members.values()], f, indent=4)

    def register(self):
        name = input("Enter your name: ")
        member_id = input("Create a member ID: ")
        if member_id in self.members:
            print("Member ID already exists.")
            return None
        password = input("Create a password: ")
        new_member = SwapMember(member_id, name, password)
        self.members[member_id] = new_member
        self.save_data()
        print("Registration successful.")
        return new_member

    def login(self):
        member_id = input("Member ID: ")
        password = input("Password: ")
        member = self.members.get(member_id)
        if member and member._password == password:
            print(f"Welcome back, {member._name}!")
            return member
        print("Invalid credentials.")
        return None

    def add_item(self):
        item_type = input("Add Topwear or Bottomwear? ").strip().lower()
        item_id = input("Enter item ID: ")
        title = input("Enter title: ")
        if item_type == "topwear":
            brand = input("Brand: ")
            size = input("Size: ")
            color = input("Color: ")
            item = Topwear(title, item_id, brand, size, color)
        elif item_type == "bottomwear":
            waist = int(input("Waist Size: "))
            length = int(input("Length: "))
            material = input("Material: ")
            item = Bottomwear(title, item_id, waist, length, material)
        else:
            print("Invalid type.")
            return
        self.items[item_id] = item
        self.save_data()
        print("Item added successfully.")

    def show_available_items(self):
        if not self.items:
            print("No items available.")
            return
        print("\nAvailable Clothing Items:")
        for item in self.items.values():
            item.display_details()

    def borrow_item(self, member):
        if not self.items:
            print("No items available to borrow.")
            return

        print("\nAvailable Items to Borrow:")
        for item in self.items.values():
            item.display_details()

        item_id = input("Enter item ID to borrow: ")
        if item_id in self.items:
            item = self.items[item_id]
            member._borrowed_items.append(item.to_dict())
            del self.items[item_id]
            self.save_data()
            print(f"You borrowed item {item_id}")
        else:
            print("Invalid item ID.")

    def return_item(self, member):
        if not member._borrowed_items:
            print("You have not borrowed any items.")
            return

        print("\nItems You've Borrowed:")
        items_to_return = []
        for i, item_data in enumerate(member._borrowed_items, start=1):
            if isinstance(item_data, dict):
                item = ClothingItem.from_dict(item_data)
            else:
                item = Topwear("Unknown", item_data, "Unknown", "Unknown", "Unknown")
            items_to_return.append((i, item_data, item))
            print(f"{i}. ", end="")
            item.display_details()

        try:
            index = int(input("Enter number of item to return: ")) - 1
            if index < 0 or index >= len(items_to_return):
                raise ValueError

            _, item_data, item = items_to_return[index]
            member._borrowed_items.remove(item_data)

            if isinstance(item_data, dict):
                item = ClothingItem.from_dict(item_data)
            else:
                print("Re-enter item details for return:")
                item_type = input("Type (Topwear/Bottomwear): ").strip().lower()
                title = input("Title: ")
                if item_type == "topwear":
                    brand = input("Brand: ")
                    size = input("Size: ")
                    color = input("Color: ")
                    item = Topwear(title, item_data, brand, size, color)
                else:
                    waist = int(input("Waist Size: "))
                    length = int(input("Length: "))
                    material = input("Material: ")
                    item = Bottomwear(title, item_data, waist, length, material)

            self.items[item.item_id] = item
            self.save_data()
            print("Item returned.")
        except ValueError:
            print("Invalid selection.")

def show_login_menu():
    print("=" * 50)
    print("|{:^48}|".format("SWAP THREADS"))
    print("|{:^48}|".format("Borrow • Exchange • Return"))
    print("=" * 50)
    print("|{:^48}|".format("1. Login"))
    print("|{:^48}|".format("2. Register"))
    print("|{:^48}|".format("3. Exit"))
    print("=" * 50)

def show_main_menu():
    print("\n" + "=" * 50)
    print("|{:^48}|".format("MAIN MENU"))
    print("=" * 50)
    print("|{:^48}|".format("1. Add Item"))
    print("|{:^48}|".format("2. View Items"))
    print("|{:^48}|".format("3. Borrow Item"))
    print("|{:^48}|".format("4. Return Item"))
    print("|{:^48}|".format("5. Logout"))
    print("=" * 50)

def main():
    app = SwapSystem()
    user = None

    while not user:
        show_login_menu()
        choice = input("Select an option (1/2/3): ").strip()
        if choice == "1":
            user = app.login()
        elif choice == "2":
            user = app.register()
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid input.")

    while True:
        show_main_menu()
        action = input("Choose an option: ").strip()
        if action == "1":
            app.add_item()
        elif action == "2":
            app.show_available_items()
        elif action == "3":
            app.borrow_item(user)
        elif action == "4":
            app.return_item(user)
        elif action == "5":
            print("Logged out.")
            app.save_data()
            break
        else:
            print("Invalid input.")

if __name__ == "__main__":
    main()
