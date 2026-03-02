from flask import render_template, redirect, url_for, flash, request
from app import app
from app import db
from app.forms import EventForm
from app.models import Event
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func