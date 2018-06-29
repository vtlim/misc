# Purpose: Take the running average of two data sets over 25 data points.
#          Modify the value 25 as desired.
# Usage: First load data, then click
#    Window > commands > read > runavg2.com > replay
# http://plasma-gate.weizmann.ac.il/Grace/doc/UsersGuide.html

runavg(s0, 25)
runavg(s1, 25)
redraw
updateall
