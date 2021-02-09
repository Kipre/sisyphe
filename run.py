import sisyphe
import os

categories = ["Art & Design",
  "Bets & Gambling",
  "Books",
  "Business & Entrepreneurship",
  "Cars & Other Vehicles",
  "Celebrities & Lifestyle",
  "Cryptocurrencies",
  "Culture & Events",
  "Curious Facts",
  "Directories of Channels & Bots",
  "Economy & Finance",
  "Education",
  "Erotic Content",
  "Fashion & Beauty",
  "Fitness",
  "Food & Cooking",
  "Foreign Language Learning",
  "Health & Medicine",
  "History",
  "Hobbies & Activities",
  "Home & Architecture",
  "Humor & Memes",
  "Investments",
  "Job Listings",
  "Kids & Parenting",
  "Marketing & PR",
  "Motivation & Self-development",
  "Movies",
  "Music",
  "Offers & Promotions",
  "Pets",
  "Politics & Incidents",
  "Psychology & Relationships",
  "Real Estate",
  "Recreation & Entertainment",
  "Religion & Spirituality",
  "Science",
  "Sports",
  "Technology & Internet",
  "Travel & Tourism",
  "Video Games",
  "Other"]
  
def render(row):
    html = f"<h3>{row['title']}</h3>"
    html += f"<p>{row['description']}</p>"
    html += f"<p>{row['recent_posts']}</p>"
    return html

labeller = sisyphe.Sisyphe('C:/Users/kipr/Downloads/example.csv', categories, render)
sisyphe.run(labeller)