import os
from pathlib import Path

import numpy as np
import pandas as pd

from ConfLearning.util.model_to_latex import latex_to_png
from regression import regression

path_data = os.path.join(Path.cwd(), '../data/')

data = pd.read_pickle(os.path.join(path_data, 'data.pkl'))

nsubjects = 66
nblocks = 11
npairs = 10
ntrials_phase0 = (9, 12, 15, 18)
ntrials_phase1 = (0, 5, 10, 15)
ntrials_phase2 = (9, 12, 15, 18)

# We're including subjects with at least 55% performance
include = np.where(np.array(100*data.groupby('subject').correct.mean().values, int) > 55)[0]
exclude = np.setdiff1d(range(nsubjects), include)
print(f"Subjects with performance < 0.55 (N={len(exclude)}, remain={nsubjects - len(exclude)}): [{', '.join([str(v) for v in exclude])}]")


map = dict(
    b_designated_absvaluediff='block_difficulty',
    b_valuebase='block_value_level',
    b_ntrials_pre='block_ntrials_phase1',
    b_ntrials_noc='block_ntrials_phase2',
    b_stimulus_pool='block_stimulus_type',
    value_chosen='value',
    ratingdiff21='rating_change',
)
d = data.copy().rename(columns=map)


ps = ['block_difficulty', 'block_value_level', 'block_stimulus_type', 'block_stimulus_type', 'block_ntrials_phase1', 'block_ntrials_phase2', 'value']
model = regression(
    d[~d.rating_change.isna() & (d.block_ntrials_phase2 > 0)],
    # patsy_string='ratingdiff ~ ' + ' + '.join(ps),
    patsy_string='rating_change ~ ' + ' + '.join(ps) + ' + value:block_ntrials_phase2',
    standardize_vars=True,
    ignore_warnings=True,
    model_blocks=True,
    reml=False,
    print_data=False
)
skip_var_hack = 'subject Var                  &  0.023 &    0.034 &        &             &        &         \\\\\nblock Var                    &  0.074 &    0.043 &        &             &        &         \\\\\n'
latex_to_png(model, outpath=os.path.join(os.getcwd(), 'regtables', f'{Path(__file__).stem}.png'),
             title=None, DV='rating\_change', skip_var_hack=skip_var_hack)