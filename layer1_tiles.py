import subprocess
import sys
import pandas as pd
import PythonMagick as Magick


def partial_sum(li, start, end):
    summ = 0
    for x in range(start, end):
        summ += li[x]
    return summ


print(sys.argv[1])
df = pd.read_csv(sys.argv[1])
#42 characters each line
max_pixel_col = 630
width_per_char = 15
height_per_char = 30
num_rows = df.shape[0]
num_cols = df.shape[1]

width_list = [0 for x in range(num_cols)]
#calculate width for each column
for x in range(0,num_cols):
    for y in range(0,num_rows):
        width = len(str(df.iloc[y][x]))*width_per_char
        if width < max_pixel_col:
            width_list[x] = max(width_list[x],width)
        else:
            width_list[x] = max_pixel_col

#calculate height of each row
height_list = [0 for x in range(num_rows)]
for x in range(0,num_rows):
    for y in range(0,num_cols):
        height = len(str(df.iloc[x][y])) // 42 * height_per_char
        if len(str(df.iloc[x][y])) % 42 != 0:
            height = height + height_per_char
        height_list[x] = max(height_list[x],height)

total_width = sum(width_list)
filename = 0

for i in range(0, num_rows, 10):
    total_height = partial_sum(height_list, i, min(num_rows, i + 10))
    image_size = str(total_width) + "x" + str(total_height)
    print(image_size)

    script = "magick#-size#" + image_size + "#-fill#white#canvas:none#-stroke#opaque#-draw#rectangle 0,0 "+str(total_width)+","+str(total_height) + "#" + str(filename) + ".png"
    splitted = script.split("#")

    subprocess.call(splitted, shell=True)

    img = Magick.Image(str(filename) + ".png")
    # draw horizontal lines
    pos1 = 0
    for x in range(i, min(num_rows, i + 10)):
        pos1 += height_list[x]
        line = Magick.DrawableLine(0, pos1, total_width, pos1)
        img.draw(line)

    # draw vertical lines
    pos2 = 0
    for x in range(0, num_cols):
        pos2 += width_list[x]
        line = Magick.DrawableLine(pos2, 0, pos2, total_height)
        img.draw(line)

    img.write(str(filename) + ".png")
    filename += 1




