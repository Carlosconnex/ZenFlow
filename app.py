from app import create_app, db  # <--- This tells Python where to find your setup
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == "__main__":
    # This block is the "Magic Wand" that creates your tables
    with app.app_context():
        db.create_all() 
        print("Database tables created successfully!")
        
    app.run(host='0.0.0.0', port=5000, debug=True)