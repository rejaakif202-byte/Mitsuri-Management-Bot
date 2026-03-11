import os
import importlib
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN


app = ApplicationBuilder().token(BOT_TOKEN).build()


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

    # folder modules load
    for folder in MODULE_FOLDERS:

        path = folder.replace(".", "/")

        for file in os.listdir(path):

            if file.endswith(".py") and not file.startswith("__"):

                module_name = f"{folder}.{file[:-3]}"

                try:
                    module = importlib.import_module(module_name)

                    if hasattr(module, "setup"):
                        module.setup(app)

                    print(f"Loaded {module_name}")

                except Exception as e:
                    print(f"Failed {module_name} → {e}")

    # single modules load
    for module_name in ROOT_MODULES:

        try:
            module = importlib.import_module(module_name)

            if hasattr(module, "setup"):
                module.setup(app)

            print(f"Loaded {module_name}")

        except Exception as e:
            print(f"Failed {module_name} → {e}")


def main():

    load_modules()

    print("StrawHatManagerBot Started Successfully")

    app.run_polling()


if __name__ == "__main__":
    main()
