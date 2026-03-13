import os
import importlib
import asyncio

from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN


app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


MODULE_FOLDERS = [
    "modules.admin",
    "modules.members",
    "modules.sudo"
]

ROOT_MODULES = [
    "modules.broadcast",
    "modules.users_saver"
]


def load_modules():

    for folder in MODULE_FOLDERS:

        path = folder.replace(".", os.sep)

        if not os.path.isdir(path):
            print(f"Folder not found: {path}")
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


async def main():

    try:

        load_modules()

        await app.start()

        print("StrawHatManagerBot Started Successfully")

        await idle()

    except Exception as e:

        print("BOT CRASHED →", e)


if __name__ == "__main__":
    asyncio.run(main())
