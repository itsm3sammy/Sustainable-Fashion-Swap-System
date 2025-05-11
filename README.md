# SwapThreads

**SwapThreads** is a terminal-based Python application that promotes sustainable fashion through a community-driven clothes swapping system. Users can register, login, add clothes, borrow items, and return borrowed clothes — all from the command line.

---

## Features

- Register and login system (credentials stored persistently)
- Add clothing items to the shared wardrobe
- Borrow available items with full details
- Return borrowed items easily
- Persistent data storage via `items.json` and `users.json`
- Clean command-line UI with boxed menus

---

## How It Works

- **Topwear and Bottomwear** are modeled as object-oriented classes with attributes like brand, size, and color.
- **Users** (Swap Members) can manage their borrowed items.
- The **SwapSystem** handles the logic for all users and clothing items.

---

## Getting Started

### Requirements
- Python 3.x

### Run the App

```bash
python main.py
```
---

## Sample Data
The items.json file includes sample clothing items like jackets, shirts, and pants.
This data was auto-generated using AI to help you quickly test the app's features.

## Missing Feature
I couldn’t add a swap credit system — it was tricky to balance points and keep it simple in a terminal app, so I skipped it for now.
