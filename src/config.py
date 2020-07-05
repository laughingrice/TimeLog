import pathlib

app_path = (pathlib.Path().home() / pathlib.Path(".local/share/TimeLog"))

# Make sure the app directory exists
app_path.mkdir(parents=True, exist_ok=True)