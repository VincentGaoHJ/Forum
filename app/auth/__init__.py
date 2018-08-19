from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import forms
from . import views
