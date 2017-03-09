from app import settings
from app.factory import create_app
import sys

app = create_app()
app.run(host='0.0.0.0', debug=True, port=8080)