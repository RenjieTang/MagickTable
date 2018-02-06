# Data Map

name still under consideration

## TOC

- [Methods and Attempts to convert table to image](#methods-and-attempts-to-convert-table-to-image)
- [Meeting notes 01/19/2018](#notes-from-meeting-on-19th)

## Notes from meeting on 19th

:date: 01/19/2018

### Status

Renji has an implementaion based on python 3.5 and imagemagick :link: https://github.com/RenjieTang/MagickTable
. This works for small tables but crashes for tables of >=300 rows with 10 attributes

### Things to look at

- Start tiling the image during rendering itself. This is as opposed to creating a large image on the server and then tiling when sending to client.
- Truncate text columns to less number of characters
- Work with really small character sizes to reduce the size of the image
- Try lower resolution

## Methods and Attempts to convert table to image

### 1. Imagemagick

First attempt by Renjie Tang is present at :link: https://github.com/RenjieTang/MagickTable

Code is in python -_requires python 3.5_

#### problem

The approach is manual

- calculating the exact (x,y) where lines have to be drawn
- converting from cell index to (x,y) to draw the strings

:bangbang: _This would mean that for different sizes of images we would need to change the factor used to calculate the exact (x,y) coordinates_

### 2. Seaborn

Seaborn is a Python visualization library based on matplotlib. It provides a high-level interface for drawing attractive statistical graphics.

:link: https://seaborn.pydata.org/

:link: https://stackoverflow.com/questions/35411414/efficiently-ploting-a-table-in-csv-format-using-python/35411880?noredirect=1#comment58525355_35411880

#### problem

This works only for numerical data. String data can't be visualized in this way

### 3. Pandas convert to png

Code in ```pandas_matplotlib.py```
:link: https://stackoverflow.com/questions/35634238/how-to-save-a-pandas-dataframe-table-as-a-png

A better looking example is in ```mpl.py```

Both these examples work for small tables, but hangs/take really long for the ```dataBig.csv``` so we can't possibly use it as is.

:question: Could we possibly tile the rendering?

### 4. Convert to HTML and then save it