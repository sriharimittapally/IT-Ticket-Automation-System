from dotenv import load_dotenv
load_dotenv()
from flask import Flask
from database.db import create_table
from routes.ticket_routes import ticket_bp

app = Flask(__name__)

# Initialize DB
create_table()

# Register routes
app.register_blueprint(ticket_bp)

@app.route('/')
def home():
    return "IT Ticket System Running"

if __name__ == '__main__':
    app.run(debug=True)