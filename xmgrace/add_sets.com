# Purpose: Add two data sets in xmgrace
# Usage: First load data, then click
#    Window > commands > read > add2.com > replay
# https://stackoverflow.com/questions/41962443/add-data-sets-with-xmgrace

s2 length s0.length
s2.x = s0.x
s2.y = s0.y+s1.y
redraw
updateall
