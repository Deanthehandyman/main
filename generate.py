import os
from datetime import datetime
import glob

# Set everything to ROOT since that's where your files are
IDEAS_FILE = 'ideas.txt'
POSTS_DIR = 'posts'
SITEMAP_FILE = 'sitemap_blogs.xml'

# Create the posts folder if it doesn't exist
if not os.path.exists(POSTS_DIR):
    os.makedirs(POSTS_DIR)

# Check if ideas.txt exists
if not os.path.exists(IDEAS_FILE):
    print("Error: ideas.txt not found in the root folder.")
    exit(1) # This tells GitHub the action failed because of a missing file

with open(IDEAS_FILE, 'r') as f:
    ideas = [line.strip() for line in f.readlines() if line.strip()]

# Process 3 blogs
if len(ideas) > 0:
    to_post = ideas[:3]
    remaining = ideas[3:]

    for idea in to_post:
        safe_name = idea.lower().replace(" ", "-").replace(":", "").replace("/", "")
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(POSTS_DIR, f"{date_str}-{safe_name}.html")
        
        blog_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{idea} | Dean's Handyman Service LLC</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; }}
        .btn {{ background: #d4af37; color: black; padding: 15px 25px; text-decoration: none; border-radius: 4px; font-weight: bold; display: inline-block; }}
    </style>
</head>
<body>
    <a href="../index.html">← Back to Home</a>
    <h1>{idea}</h1>
    <p>Dean's Handyman Service LLC provides professional help with <strong>{idea}</strong> in Pittsburg and East Texas.</p>
    <br>
    <a href="https://deanshandymanservice.me" class="btn">Get a Quote</a>
</body>
</html>"""
        
        with open(filename, 'w') as f:
            f.write(blog_content)

    # Update ideas.txt
    with open(IDEAS_FILE, 'w') as f:
        f.write('\n'.join(remaining))

# Generate Sitemap
all_posts = glob.glob(os.path.join(POSTS_DIR, "*.html"))
with open(SITEMAP_FILE, 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for post in all_posts:
        f.write(f'  <url><loc>https://deanthehandyman.github.io/posts/{os.path.basename(post)}</loc></url>\n')
    f.write('</urlset>')
