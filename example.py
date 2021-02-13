import sisyphe
import pandas as pd

folder_path = "C:/Users/kipr/Downloads/"

categories = ["Art & Design", "Bets & Gambling", "Books",
  "Business & Entrepreneurship", "Cars & Other Vehicles",
  "Celebrities & Lifestyle", "Cryptocurrencies", "Culture & Events",
  "Curious Facts", "Directories of Channels & Bots", "Economy & Finance",
  "Education", "Erotic Content", "Fashion & Beauty", "Fitness",
  "Food & Cooking", "Foreign Language Learning", "Health & Medicine",
  "History", "Hobbies & Activities", "Home & Architecture",
  "Humor & Memes", "Investments", "Job Listings", "Kids & Parenting",
  "Marketing & PR", "Motivation & Self-development", "Movies",
  "Music", "Offers & Promotions", "Pets", "Politics & Incidents",
  "Psychology & Relationships", "Real Estate", "Recreation & Entertainment",
  "Religion & Spirituality", "Science", "Sports", "Technology & Internet",
  "Travel & Tourism", "Video Games", "Other", "Not Eng-Rus"]
  
def render(row):
    html = f"<h3>{row['title']}</h3>"
    html += f"<p>{row['description']}</p>"
    html += f"<p>{row['recent_posts']}</p>"
    return html

data = pd.read_csv(folder_path + 'example.csv', index_col=0)

def save_callback(labels):
    df = pd.DataFrame.from_dict(labels, orient='index')
    df.to_csv(folder_path + 'label.csv')


labeller = sisyphe.Sisyphe(data.to_dict('index'),
                           categories,
                           folder_path + 'log.tsv',
                           save_callback,
                           render_callback=render,
                           multilabel=True)
sisyphe.run(labeller)