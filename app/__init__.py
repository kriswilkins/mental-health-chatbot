from quart import Quart, session # type: ignore

app = Quart(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

from app import routes
