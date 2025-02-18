from . import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_date = db.Column(db.Date, nullable=False, index=True)
    content = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Note {self.id} for {self.note_date}>"
