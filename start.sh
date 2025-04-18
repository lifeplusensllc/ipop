if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/Learningbots79/movies.git /movies
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /movies
fi
cd /TheMovieProviderBot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
