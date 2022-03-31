import os
os.environ['MPLCONFIGDIR'] = os.getcwd() + "/configs/"
import matplotlib.pyplot as plt
import seaborn as sns

# reading in the datafile
with open('data/music.csv', 'r') as text_file:
  data_list = text_file.readlines()

keys = data_list.pop(0)
#print(data_list)

def keyIndex(keys, key):
  '''
        In order to find a key given on CORGIS website, we need to search for the key here that will return the
        associated column number. It should return a value between 0 and 34 (I think) and if something goes horribly
        wrong it will send -1. Seems good...
  '''
  pieces = keys.replace('"', "").split(',')

  for i in range(0, len(pieces)):
    if key in pieces[i]:
      return i
  # if we don't find the key, return unusable value
  return -1

time_signatures   = { }
tsIndex = keyIndex(keys, "song.time_signature")
popularity_by_ts  = { }
pIndex = keyIndex(keys, "song.hotttnesss")

# lists for question 3
ts = []
hotness = []
# this loop will strip the quotes off the strings and fill up these dictionaries and lists for future graphs
for str in data_list:
  pieces    = str.replace('"', "").split(',')
  time_sig  = float(pieces[tsIndex])
  song_pop  = float(pieces[pIndex])

  # unconditionally add these for scatterplot later
  ts.append(time_sig)
  hotness.append(song_pop)

  # i don't want these various "-1" values that are returned, nor do i care about any measures
  # that have 1 or less bar in them
  if time_sig > 1 and time_sig in time_signatures.keys() and song_pop >= 0:
    time_signatures[time_sig] += 1
  elif time_sig > 1 and song_pop >= 0:
    time_signatures[time_sig] = 1
  # in this part, it will instead fill up the "popularity" values that we can later do something with
  if time_sig > 1 and time_sig in popularity_by_ts.keys() and song_pop >= 0:
    popularity_by_ts[time_sig] += song_pop
  elif time_sig > 1 and song_pop >= 0:
    popularity_by_ts[time_sig] = song_pop
# (1) How many time signatures are in the file?
print("(1) There are", len(time_signatures), "time signatures (greater than 1 beat per bar) in the file")

# make some more lists, maybe redundant
ts_list = list(time_signatures.keys())
ts_count = list(time_signatures.values())
tsp_list = list(popularity_by_ts.keys())
tsp_count = list(popularity_by_ts.values())

# (2) What time signature was the most popular based on popularity of songs in that signature?
avgPop = []
for i in range(3, 8):
  if (i != 6):
    avgPop.append(popularity_by_ts[i] / time_signatures[i])
    print ("(2)" + chr(94+i) + ". The average popularity of a song in", i, "is", popularity_by_ts[i] / time_signatures[i])

# box plot showing the outlier is the standard time signature 4/4
# meaning 3, 5, and 7 are more closely similar as we will later see
plt.boxplot(avgPop)
plt.title('Average Popularity (0-1) per Time Signature')
plt.savefig('boxplot.png')
block = False
plt.show()
print("(2) boxplot. There is 1 outlier -- which is the most popular time signature of 4/4")

# bar chart showing the number of songs in each time signature.
# it is clear that there are many more 4/4 songs than any other signature.
# in fact more than twice the amount of the rest -- and this isn't including
# several points of data that were removed by refining it to > 1 beat per bar
# in an effort to get true meaning of this data, but will include these later in scatterplot
my_graph = sns.barplot(x = ts_list, y = ts_count)
my_graph.set(xlabel="Time Signatures (Beats per bar)", ylabel="Number of Songs")
plt.savefig("barchart.png")

# (3) Is there a correlation between time signature and popularity?
print("(3) No linear correlation is present, but odd numbers are notably less preferred)")
plt.figure(figsize=(7,4))
scatter_graph = sns.scatterplot(x = ts, y = hotness)
scatter_graph.set(ylabel = 'Popularity of Song')
scatter_graph.set(xlabel = 'Time Signature')
plt.savefig("scatterplot.png")
print("(3)a. The points represent the popularity of a song, given its time signature")
print("(3)b-c. the x axis is measuring the time signature, the y the popularity or 'hotness'.")
print("(3)d. There is either no association, or a bell curve, but one trend is that odd numbers are less potent")
print("(3)e. There are a few outliers, which seem to be misentered data -- things with 0-.5 beats per measure")
print("(3)f. also, there was no note as to what these -1 values even mean, but those would be outliers if I really thought they should be considered part of the data -- but they seem to be errors that the machine that made the database couldn't determine popularity")