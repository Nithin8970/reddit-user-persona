import praw
import re
from textblob import TextBlob
from urllib.parse import urlparse
from collections import Counter

# --- Reddit API Credentials ---
REDDIT_CLIENT_ID = '_H9vmUGDkaxtAYN_WU9j3A'
REDDIT_CLIENT_SECRET = 'JR_UWniDh0-xkxOabLo0CJVWhg8KXQ'
REDDIT_USER_AGENT = 'reddit-persona-script by u/Haunting-Donut-6244'

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def extract_username_from_url(url):
    return urlparse(url).path.split("/")[2]

def analyze_text_for_traits(text):
    traits = {}
    # Age
    age = re.findall(r"\b(?:I'?m|I am|I'm) (\d{1,2})\b", text)
    if age:
        traits["Age"] = (age[0], text)

    # Location
    location = re.findall(r"(?:from|live in|based in)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)", text)
    if location:
        traits["Location"] = (location[0], text)

    # Profession
    job = re.findall(r"(?:I work as|I'?m a|I am a)\s+([a-zA-Z ]{3,30})", text)
    if job:
        traits["Occupation"] = (job[0], text)

    return traits

def generate_persona(username):
    user = reddit.redditor(username)
    traits = {}
    posts = []
    behaviours = []
    frustrations = []
    goals = []
    quotes = []
    tones = []

    interests = set()
    citations = []

    for comment in user.comments.new(limit=100):
        text = comment.body
        found = analyze_text_for_traits(text)
        for k, (val, source) in found.items():
            if k not in traits:
                traits[k] = {"value": val, "source": f"Comment: \"{source[:80]}...\" (https://reddit.com{comment.permalink})"}
        blob = TextBlob(text)
        tones.append(blob.sentiment.polarity)
        posts.append((text, "comment", comment.permalink))
        interests.add(comment.subreddit.display_name)
        if len(text.split()) > 12:
            quotes.append(text.strip())

    for submission in user.submissions.new(limit=50):
        text = submission.title + " " + submission.selftext
        found = analyze_text_for_traits(text)
        for k, (val, source) in found.items():
            if k not in traits:
                traits[k] = {"value": val, "source": f"Post: \"{source[:80]}...\" (https://reddit.com{submission.permalink})"}
        blob = TextBlob(text)
        tones.append(blob.sentiment.polarity)
        posts.append((text, "post", submission.permalink))
        interests.add(submission.subreddit.display_name)
        if len(text.split()) > 12:
            quotes.append(text.strip())

    # Inferred traits
    tone_label = "Positive" if sum(tones)/len(tones) > 0.3 else "Negative" if sum(tones)/len(tones) < -0.3 else "Neutral"
    traits["Personality"] = {"value": tone_label, "source": "Average sentiment from posts/comments"}

    traits["Interests"] = {"value": ", ".join(list(interests)[:5]), "source": "Frequent subreddit participation"}

    # Behavior & goals from top patterns
    for text, _, _ in posts:
        if "struggling" in text or "balance" in text:
            frustrations.append("Struggles with balance between life, health, or career.")
        if "learning" in text or "studying" in text:
            behaviours.append("Invests time in self-learning and skill development.")
            goals.append("Wants to improve career prospects through continuous learning.")
        if "feel lonely" in text or "isolated" in text:
            frustrations.append("Feels isolated or disconnected.")
        if "help others" in text or "explain" in text:
            goals.append("Enjoys helping others through explanations or advice.")

    # Clean duplicates
    frustrations = list(set(frustrations))[:5]
    behaviours = list(set(behaviours))[:5]
    goals = list(set(goals))[:5]

    # Pick a sample quote
    sample_quote = quotes[0] if quotes else "No quote available."

    return traits, behaviours, frustrations, goals, sample_quote

def save_qualitative_persona(username, traits, behaviours, frustrations, goals, quote):
    filename = f"user_persona_{username}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("                USER PERSONA\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")

        f.write(f"Username: u/{username}\n")
        f.write(f"Age: {traits.get('Age', {}).get('value', '[Not found]')}\n")
        f.write(f"Occupation: {traits.get('Occupation', {}).get('value', '[Not found]')}\n")
        f.write(f"Location: {traits.get('Location', {}).get('value', '[Not found]')}\n")
        f.write("Tier: Early Adopter\n")
        f.write("Archetype: The Explorer\n\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write(f"QUOTE:\n\"{quote}\"\n\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("TRAITS:\n")
        for key in ["Personality", "Interests"]:
            if key in traits:
                f.write(f"- {key}: {traits[key]['value']} (Source: {traits[key]['source']})\n")
        f.write("\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("BEHAVIOUR & HABITS:\n")
        for b in behaviours or ["[Not enough data]"]:
            f.write(f"• {b}\n")
        f.write("\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("FRUSTRATIONS:\n")
        for fstr in frustrations or ["[No major frustrations found]"]:
            f.write(f"• {fstr}\n")
        f.write("\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("GOALS & NEEDS:\n")
        for g in goals or ["[No goals inferred]"]:
            f.write(f"• {g}\n")
        f.write("\n")

        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
        f.write("CITATIONS:\n")
        for key, value in traits.items():
            if "source" in value:
                f.write(f"- {key}: {value['source']}\n")
        f.write("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

    print(f"[✓] Persona saved to: {filename}")

# --- MAIN ---
if __name__ == "__main__":
    url = input("Enter Reddit profile URL: ")
    username = extract_username_from_url(url)
    traits, behaviours, frustrations, goals, quote = generate_persona(username)
    save_qualitative_persona(username, traits, behaviours, frustrations, goals, quote)
