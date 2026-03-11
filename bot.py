import os
import importlib
from telegram.ext import ApplicationBuilder
from config import BOT_TOKEN


# ================= BOT START =================

app = ApplicationBuilder().token(BOT_TOKEN).build()


# ================= LOAD MODULES =================

MODULES = [
    "modules.admin",
    "modules.members",
    "modules.sudo",
    "modules.media"
]


def load_modules():

    for module in MODULES:

        path = module.replace(".", "/")

        if not os.path.isdir(path):
            continue

        for file in os.listdir(path):

            if file.endswith(".py") and not file.startswith("__"):

                module_name = f"{module}.{file[:-3]}"

                try:
                    imported = importlib.import_module(module_name)

                    if hasattr(imported, "setup"):
                        imported.setup(app)

                    print(f"Loaded {module_name}")

                except Exception as e:
                    print(f"Failed to load {module_name} : {e}")


# ================= MAIN =================

def main():

    load_modules()

    print("StrawHatManagerBot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
