# routes.py
from datetime import datetime, timedelta

import markdown
from flask import Blueprint, flash, redirect, render_template, request, url_for

from . import db
from .models import Note

main_bp = Blueprint("main", __name__)


@main_bp.route("/date/<note_date>", methods=["GET", "POST"])
def notebook(note_date):
    # Validate and parse the date
    try:
        current_date = datetime.strptime(note_date, "%Y-%m-%d").date()
    except ValueError:
        flash("Invalid date format. Use YYYY-MM-DD.")
        return redirect(url_for("main.index"))

    # Fetch or create the note for this date
    note = Note.query.filter_by(note_date=current_date).first()
    if not note:
        note = Note(note_date=current_date, content="")
        db.session.add(note)
        db.session.commit()

    # Handle form submission (updating note content)
    if request.method == "POST":
        content = request.form.get("content", "")
        note.content = content
        db.session.commit()
        flash("Note saved!")
        # After saving, redirect to the same page (still in preview mode)
        return redirect(url_for("main.notebook", note_date=note_date))

    # Convert markdown to HTML for preview
    rendered_content = markdown.markdown(note.content) if note.content else ""

    # Format date components
    day = current_date.day
    month = current_date.strftime("%B")
    year = current_date.year

    # Calculate next/previous day for navigation
    next_day = current_date + timedelta(days=1)
    prev_day = current_date - timedelta(days=1)
    next_day_str = next_day.strftime("%Y-%m-%d")
    prev_day_str = prev_day.strftime("%Y-%m-%d")

    return render_template(
        "notebook.html",
        note=note,
        rendered_content=rendered_content,
        day=day,
        month=month,
        year=year,
        next_day_str=next_day_str,
        prev_day_str=prev_day_str,
    )
