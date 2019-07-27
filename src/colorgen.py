# colorgen.py
#
# Copyright 2011 West - License: Public domain
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import math
import itertools
from decimal import *

# if len(sys.argv) != 2:
#   print Usage: colorgen.py NumberOfColors
#   sys.exit()
# second arg is number of colors to 
# if num < 1:
#   print("Error: Stop screwing around.")
#   sys.exit()
  
def MidSort(lst):
  if len(lst) <= 1:
    return lst
  i = int(len(lst)/2)
  ret = [lst.pop(i)]
  left = MidSort(lst[0:i])
  right = MidSort(lst[i:])
  interleaved = [item for items in itertools.zip_longest(left, right)
    for item in items if item != None]
  ret.extend(interleaved)
  return ret

def getColours(num):
    # Build list of points on a line (0 to 255) to use as color 'ticks'
    max = 255
    segs = int(num**(Decimal("1.0")/3))
    step = int(max/segs)
    p = [(i*step) for i in range(1,segs)]
    points = [0,max]
    points.extend(MidSort(p))

    # Not efficient!!! Iterate over higher valued 'ticks' first (the points
    #   at the front of the list) to vary all colors and not focus on one channel.
    colors = ["%02X%02X%02X" % (points[0], points[0], points[0])]
    tempRange = 0
    total = 1
    while total < num and tempRange < len(points):
        tempRange += 1
        for c0 in range(tempRange):
            for c1 in range(tempRange):
                for c2 in range(tempRange):
                    if total >= num:
                        break
                    c = "%02X%02X%02X" % (points[c0], points[c1], points[c2])
                    if c not in colors:
                        colors.append(c)
                        total += 1
            
    return colors