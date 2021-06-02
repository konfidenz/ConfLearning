import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from scipy import stats

cwd = Path.cwd()
path_data = os.path.join(cwd, '../../results/fittingData')

conf_slope = np.load('confSlope_5-15.npy')

model_name = ['Rescorla\nConf', 'Rescorla\nConfGen', 'Rescorla\nConfNoFeed', 'Rescorla\nConfNoFeedGen',
              'Rescorla\nConfZero', 'Rescorla\nConfZeroGen', 'Rescorla\nConfNoFeedZero', 'Rescorla\nConfNoFeedZeroGen']

modellist = np.arange(2, 10)
nsubjects = 66

fig, axes = plt.subplots(4, 2, figsize=(20, 10))
rows, columns = [*[0 for _ in range(2)], *[1 for _ in range(2)], *[2 for _ in range(2)], *[3 for _ in range(2)]], [0, 1, 0, 1, 0, 1, 0, 1]

for m, model in enumerate(modellist):

    fittingData = pd.read_pickle(os.path.join(path_data, 'fittingDataM' + str(model) + '.pkl'))
    row, col = rows[m], columns[m]

    rho, pval = stats.spearmanr(fittingData.ALPHA_C, conf_slope)
    axes[row, col].scatter(fittingData.ALPHA_C, conf_slope, s=8, c='g', marker='o')
    # axes[row, col].set_title(model_name[m])
    axes[row, col].set_xlabel('gamma')
    axes[row, col].set_ylabel('confidence slope (5-15 trials)')
    # axes[row, col].set_xticks(np.arange(0, 1.1, step=0.2))
    axes[row, col].set_yticks(np.arange(-0.75, 0.76, step=0.25))
    axes[row, col].text(3, -0.5 if rho >= 0 else -0.5, 'rho = ' + str(round(rho, 2)) + ', p = ' + str(round(pval, 2)), color='k', fontsize=10)
    axes[row, col].grid('silver', linestyle='-', linewidth=0.4)
fig.savefig('../../figures/validation/conf_slope/corr_conf_slope_5-15_gamma.png', bbox_inches='tight')
plt.close()
