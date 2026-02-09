# CommentBot
A simple design for a telegram bot that randomly replies to group chat members with desired text.
# Set Up
Clone the repository with ``` git clone https://github.com/MattTheGreat-root/CommentBot.git ``` then ``` cd CommentBot ```
## Configure
Add the texts you want to be replied to users in the ``` comments.text ```.
You can change the frequency of the replies by changing ``` random.randint(1, 15) == 1 ``` in ``` async def roast(update: Update, context: ContextTypes.DEFAULT_TYPE) ``` function.
## Run
1. Build a telegram bot via "@BotFather" and save the API token.
2. Go to Render.com and choose a web service. The free tier includes 500 Mb of RAM and 0.1 CPU which is enough for this project.
3. Connect the web service with your repository and deploy it.
