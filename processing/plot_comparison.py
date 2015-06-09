import numpy as np
from pylab import *

mata = """
<acknowledgement>   1.0000  0.0000  1.0000  0.0000  0.0000  0.0000  0.0000  0.0000  1.0000
<annex> 0.0000  0.6727  0.4301  0.0000  0.9677  1.0000  0.0323  0.0000  0.4670
<body>  0.0000  0.1719  0.9473  0.0062  0.0025  0.0951  0.0037  0.0014  0.0493
<cover> 0.0000  0.0000  0.0000  1.0000  0.0000  0.0000  0.0000  0.0000  0.0000
<footnote>  0.0000  0.4135  0.7080  0.0000  0.6553  0.4193  0.0000  0.0333  0.0833
<header>    0.0000  0.0000  0.5891  0.1860  0.0000  0.9407  0.0000  0.0000  0.0000
<headnote>  0.0000  0.0941  0.5296  0.0000  0.3000  0.1013  0.6681  0.0000  0.0893
<page>  0.0000  0.0895  0.5368  0.0000  0.0000  0.1254  0.0000  0.8409  0.1333
<references>    0.8261  0.0000  0.5556  0.0000  0.0000  0.1739  0.0588  0.0000  0.9919
"""

matb = """
<acknowledgement>   1.0000  0.0000  1.0000  0.0000  1.0000  0.0000  0.0000  0.0000  0.0000
<annex> 0.0000  0.0000  0.8256  0.0000  0.1744  0.0000  0.0000  0.0000  1.0000
<body>  0.0000  0.0832  0.9796  0.0000  0.0011  0.0278  0.0041  0.0035  0.0040
<cover> 0.0000  0.0000  0.0000  1.0000  0.0000  1.0000  0.0000  0.0000  0.0000
<footnote>  0.0000  0.1536  0.6594  0.0000  0.2533  0.6790  0.3238  0.0531  0.1007
<header>    0.0000  0.0000  0.5428  0.3488  0.0000  0.9377  0.0237  0.0120  0.0000
<headnote>  0.0000  0.1053  0.4566  0.0000  0.1241  0.1603  0.7212  0.1579  0.1691
<page>  0.0000  0.0905  0.4325  0.0233  0.0000  0.0610  0.1381  0.8754  0.1391
<references>    0.4806  0.5880  0.4378  0.0000  0.0209  0.0000  0.0217  0.0107  0.8292
"""

labels = [row.split()[0].strip('<>') for row in filter(bool, mata.split('\n'))]

countsa = np.array([map(lambda x: float(x), row.split()[1:]) for row in
                    filter(bool, mata.split('\n'))])

countsb = np.array([map(lambda x: float(x), row.split()[1:]) for row in
                    filter(bool, matb.split('\n'))])

figure()
# Keep major ticks labeless
xticks(range(len(labels)), [])
yticks(range(len(labels)), [])
# Place labels on minor ticks
gca().set_xticks([x + 0.5 for x in range(len(labels))], minor=True)
gca().set_xticklabels(labels, rotation='90', fontsize=8, minor=True)
gca().set_yticks([y + 0.5 for y in range(len(labels))], minor=True)
gca().set_yticklabels(labels[::-1], fontsize=8, minor=True)
# Finally, hide minor tick marks...
gca().tick_params('both', width=0, which='minor')

counts = countsa - countsb
pcolor(array(counts[::-1]), cmap=cm.coolwarm)

for y in range(len(labels)):
    for x in range(len(labels)):
        if counts[::-1][y][x] != 0:
            text(x + 0.5, y + 0.5, counts[::-1][y][x],
                 fontsize=6,
                 horizontalalignment='center',
                 verticalalignment='center')

grid(True)
title('mata - matb')
plt.tight_layout()
savefig('comparison.pdf')
close()
