import subprocess
import sys
import pandas as pd


# magick_script = "magick#-size#" + image_size + "#canvas:none#-stroke#snow#-draw#rectangle 0,0 "+str(height)+","+str(width)+"#" \
#                 "-draw#line 0,50 400,50#-draw#line 0,100 400,100#-draw#line 0,150 400,150#-draw#line 0,200 400,200#" \
#                 "-draw#line 0,250 400,250#-draw#line 0,300 400,300#-draw#line 0,350 400,350#-draw#line 100,0 100,400#" \
#                 "-draw#line 200,0 200,400#-draw#line 300,0 300,400#-draw#text 500,500 \'yesys\'#abc.png"



print(sys.argv[1])
df = pd.read_csv(sys.argv[1]);
num_rows = df.shape[0]
num_cols = df.shape[1]
image_size = "1920x1920"
height = 1920
width = 1920

script = "magick#-size#" + image_size + "#canvas:none#-stroke#snow#-draw#rectangle 0,0 "+str(height)+","+str(width)+"#"


for x in range(1, num_rows+1):
    script += "-draw#line 0," + str(height/num_rows*x) + " " + str(width) + "," + str(height/num_rows*x) + "#"
for x in range(1,num_cols+1):
    script += "-draw#line " + str(width/num_cols*x) + ",0 " + str(width/num_cols*x) + "," +  str(height) + "#"
script += "-pointsize#60#"
for x in range(0,num_rows):
    for y in range(0,num_cols):
        script += "-draw#text " + str(width/num_cols*y + 80) + "," + str(height/num_rows*x + 80) + "\'" + str(df.iloc[x][y]) + "\'#"
script += "abc.png"

splitted = script.split("#")

subprocess.call(splitted, shell=True)
