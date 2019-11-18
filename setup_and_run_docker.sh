# Build image
docker build -t popwordsearch:demo .

# Run app
docker run -t -p 8000:8000 popwordsearch:demo

# Notification
echo "Go to localhost:8000 in your web browser to use the app"