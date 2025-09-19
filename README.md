# Telegram Ads Bot

A **Telegram bot** for creating and browsing advertisements, built as a learning project.  
It allows users to create text, photo, audio, and voice ads and browse all saved ads.  
Command handling is encapsulated in controllers, utilities cover shared logic, and middlewares extend bot behavior.

---

## ⚙️ Technical Stack

- **Python 3.10+**  
- **Aiogram**  
- **python-dotenv**  

---

## 🚀 Setup & Verification

Follow these steps to set up the project locally.  
The project was tested with **Arch Linux**, but should work on other Linux distributions if `python3` and `pip3` are available in `PATH`.

### 1. Clone the Repository

```bash
git clone https://github.com/DrArzter/telegram-bot
cd telegram-bot
````

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Then add your **Telegram Bot Token** inside `.env`.

### 4. Run the Bot

```bash
python3 src/main.py
```

---

## 📡 Usage Examples

* `/start` – Initialize the bot
* `/help` – Show available commands
* `/add` – Create a new advertisement
* `/list` – Browse all saved ads

Supports text, photos, audio, and voice messages.

---

## 🏗️ Project Structure

```markdown
src/
├── controllers/
│   ├── add.py
│   ├── callbacks.py
│   ├── help.py
│   ├── list.py
│   ├── media.py
│   └── start.py
├── middleware/
│   └── logging.py
├── services/
│   ├── keyboards.py
│   ├── logger.py
│   ├── set_commands.py
│   └── storage.py
└── main.py
```

---
