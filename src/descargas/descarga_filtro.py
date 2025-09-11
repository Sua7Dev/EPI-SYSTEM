import streamlit as st
import pandas as pd
import sqlite3
import datetime
from fpdf import FPDF
from io import BytesIO
import numpy as np
import re
import locale

DB_PATH = 'hospital.db'
DATE_FORMAT = 'DD/MM/YYYY'

