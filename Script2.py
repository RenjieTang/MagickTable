import subprocess
import sys
import pandas as pd


# magick_script = "magick#-size#" + image_size + "#canvas:none#-stroke#snow#-draw#rectangle 0,0 "+str(height)+","+str(width)+"#" \
#                 "-draw#line 0,50 400,50#-draw#line 0,100 400,100#-draw#line 0,150 400,150#-draw#line 0,200 400,200#" \
#                 "-draw#line 0,250 400,250#-draw#line 0,300 400,300#-draw#line 0,350 400,350#-draw#line 100,0 100,400#" \
#                 "-draw#line 200,0 200,400#-draw#line 300,0 300,400#-draw#text 500,500 \'yesys\'#abc.png"



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
        height = len(str(df.iloc[x][y])) / 42 * height_per_char
        if len(str(df.iloc[x][y])) % 42 != 0:
            height = height + height_per_char
        height_list[x] = max(height_list[x],height)
        #build new string if need >1 line
        # if len(str(df.iloc[x][y])) > 42:
        #     st = ""
        #     for index in range(0, len(str(df.iloc[x][y]))):
        #         st += str(df.iloc[x][y])[index]
        #         if index % 42 == 0 and index != 0:
        #             st += '\n'
        #     print(st)
            # df.iloc[x][y] = st


total_width = sum(width_list)
total_height = sum(height_list)
image_size = str(total_width) + "x" + str(total_height)
print(image_size)

script = "magick#-size#" + image_size + "#-fill#white#canvas:none#-stroke#opaque#-draw#rectangle 0,0 "+str(total_width)+","+str(total_height)+"#"

#draw horizontal lines
pos1 = 0
for x in range(1, num_rows+1):
    pos1 += height_list[x-1]
    script += "-draw#line 0," + str(pos1) + " " + str(total_width) + "," + str(pos1) + "#"
#draw vertical lines
pos2 = 0
for x in range(1,num_cols+1):
    pos2 += width_list[x-1]
    script += "-draw#line " + str(pos2) + ",0 " + str(pos2) + "," +  str(total_width) + "#"




# draw text
script += "-fill#black#-pointsize#20#-font#Times-New-Roman#"
positionhei = 0
for x in range(0,num_rows):
    positionwid = 0
    for y in range(0,num_cols):
        original_st = str(df.iloc[x][y])
        if len(original_st) > 42:
            st = ""
            for index in range(0, len(original_st)):
                st += original_st[index]
                if index % 42 == 0 and index != 0:
                    st += '\\n'
            original_st = st
        script += "-draw#text " + str(positionwid + 8) + "," + str(positionhei + 20) + "\'" + str(original_st) + "\'#"
        positionwid += width_list[y]
    positionhei += height_list[x]
script += "abc.png"


splitted = script.split("#")

subprocess.call(splitted, shell=True)
