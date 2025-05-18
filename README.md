# Calibre Book Synchronizer
This complement for Calibre enables user to select one folder as a book source folder, all books won't be moved or deleted once they're imported and any change on the original folder will be synced with your Calibre Library.

I haven't found anything similar on Calibre and that's the reason why I created this complement.

> [!WARNING]
> This complement has only been tested in Linux, specifically Arch Linux, it may not work on other distros and other Unix systems.
> Most likely this plugin won't work on Windows, however if you want to add support for it, feel free to fork or propose a PR.

## Setup & Installation for local development

1. **Create virtual env:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **For using the plugin:**
   - Follow Calibre's instructions for installing custom plugins.
   - Run Calibre and enable the plugin from the interface.