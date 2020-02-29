# Imports
import pandas as pd
import numpy as np
import glob
import re
import pickle
from datetime import datetime


# Load all company transcripts
all_transcripts = glob.glob("data/company_transcripts/*")
df = [pd.read_json(f) for f in all_transcripts]

# Pre-processing functions


def get_quarter(title):
    quarter_reg_expr = "([A-Za-z]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)"
    words = re.findall(quarter_reg_expr, title)

    def has_numbers(inputString):
        return any(char.isdigit() for char in inputString)

    for word in words:
        if "q" in word.lower() and has_numbers(word):
            return word
            # Handle Q1 vs 1Q case
            if len(word) == 2:
                if word[0] in "1234":
                    return word[1] + word[0]
                else:
                    return word
            # Handle case with F
            elif word[0] == "F":
                return word[2] + word[1]
    return None


def get_ticker(row, _id):
    title = row['title'][_id]
    body = ' '.join(row['body'][_id])

    try:
        # Try to get ticker from title
        open_paren = title.index("(")
        close_paren = title.index(")")
        return title[open_paren+1:close_paren]

    except:
        # find ticker in body
        colon = body.index(":")
        close_paren = body.index(")")
        return body[colon+1:close_paren]


# Clean
rows_list = []

for row in df:
    ids = list(row['title'].keys())

    for _id in ids:
        title = row['title'][_id]
        full_date = row['date'][_id]

        ticker = get_ticker(row, _id)
        quarter = get_quarter(title)
        date = full_date.date().strftime("%Y-%m-%d")
        time = full_date.time().strftime("%H:%M")
        body = ' '.join(row['body'][_id])

        # There are 10 titles without an explicit quarter
        if quarter is None:
            quarter = "FILL ME IN"

        new_row = [ticker, quarter, date, time, body]

        rows_list.append(new_row)

df_transcripts = pd.DataFrame(
    rows_list, columns=["ticker", "quarter", "date", "time", "body"])

with open("transcripts.p", "wb") as f:
    pickle.dump(df_transcripts, f)
