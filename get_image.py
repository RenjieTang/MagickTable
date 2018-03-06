import urllib
from bs4 import BeautifulSoup
import webbrowser
import pandas as pd
import imgkit as img

df = pd.read_csv("short.csv")
html = df.to_html()
img.from_string(html, "out.png")