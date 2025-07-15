# Reddit User Persona Generator 🧠

This Python script analyzes a Reddit user's public activity (posts/comments) and creates a detailed **user persona**, including age, location, occupation, interests, personality, goals, and frustrations — with citations pulled from their actual posts.

> ✅ This submission was prepared for the **BeyondChats AI/LLM Engineer Internship Assignment**.

---

## 📦 Features

- 🔍 Scrapes user posts and comments using Reddit API (via PRAW)
- 🧠 Extracts:
  - Age
  - Occupation
  - Location
  - Interests (via subreddits)
  - Personality sentiment
  - Behavior, Goals, Frustrations
- 📝 Outputs a **UX-style qualitative persona** in `.txt` format
- 📌 Cites each trait with the original Reddit comment or post

How to Run
1. Clone this Repo
git clone https://github.com/yourusername/reddit-user-persona.git
cd reddit-user-persona
2. Install Dependencies
pip install -r requirements.txt
3. Create Reddit API Credentials
You’ll need Reddit API access to fetch user data.

Go to: https://www.reddit.com/prefs/apps

Click "Create App"

Select script

Use: http://localhost:8080 as the redirect URI

After creation, you’ll get:

client_id

client_secret
4. Paste Credentials in main.py
Open main.py and update these lines:

REDDIT_CLIENT_ID = 'your_client_id'
REDDIT_CLIENT_SECRET = 'your_client_secret'
REDDIT_USER_AGENT = 'reddit-persona-script by u/your_reddit_username'
5. Run the Script
python main.py
When prompted, paste a Reddit profile URL:

https://www.reddit.com/user/kojied/
✅ Output: user_persona_kojied.txt is created in your folder.

🧠 Technologies Used
Python 3.7+

praw: Reddit API wrapper

textblob: Sentiment analysis

 Example Users
This submission includes:

user_persona_kojied.txt

user_persona_Hungry-Move-6603.txt

These were generated using the official example profiles shared in the assignment brief.

📬 Author
Nithin M
Assignment for BeyondChats Internship – AI/LLM Engineer Role
Date: July 2025

📜 License
This project is your property. BeyondChats will only use this code if you're selected for the paid internship.