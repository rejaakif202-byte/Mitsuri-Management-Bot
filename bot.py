import os
import importlib

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN


app = Client(
    "StrawHatManagerBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# folders jaha modules hain
MODULE_FOLDERS = [
    "modules.admin",
    "modules.members",
    "modules.sudo"
]

# single modules
ROOT_MODULES = [
    "modules.broadcast",
    "modules.users_saver"
]


def load_modules():

    for folder in MODULE_FOLDERS:

        path = folder.replace(".", "/")

        if not os.path.isdir(path):
            continue

        for file in os.listdir(path):

            if file.endswith(".py") and not file.startswith("__"):

                module_name = f"{folder}.{file[:-3]}"

                try:
                    importlib.import_module(module_name)
                    print(f"Loaded {module_name}")

                except Exception as e:
                    print(f"Failed {module_name} → {e}")


    for module_name in ROOT_MODULES:

        try:
            importlib.import_module(module_name)
            print(f"Loaded {module_name}")

        except Exception as e:
            print(f"Failed {module_name} → {e}")


def main():

    load_modules()

    print("StrawHatManagerBot Started Successfully")

    app.run()


if __name__ == "__main__":
    main()
