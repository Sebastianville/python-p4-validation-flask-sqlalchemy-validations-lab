from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def validate_author(self, key, name):
        if len(name) < 1:
            raise ValueError("Name must be at least 1 character")
        elif Author.query.filter_by(name=name).first():
            raise ValueError("Author name already exists")
        return name 
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not len(phone_number) == 10 or not phone_number.isdigit():
            raise ValueError("phone number has to be 10 digits")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def validate_content(self, key, content): 
        if len(content) < 250: 
            raise ValueError('the content has to be at least 250 characters long')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250: 
            raise ValueError('summary has to be less than or equal to 250')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        # if category != 'Fiction' and category != 'Non-Fiction' it is another way to write this
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category has to be either ficiton or non-fiction')
        return category 
    
    @validates("title")
    def validate_title(self, key, title):
        for clickbait in ["Won't Believe", "Secret", "Top", "Guess"]:
            if clickbait in title:
                return title
        raise ValueError(
            "Title must contain 'Won't Believe', 'Secret', 'Top', or 'Guess'"
        ) 



    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
