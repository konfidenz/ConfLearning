import os
from pathlib import Path

import numpy as np
import pandas as pd

from regression import regression
from ConfLearning.util.model_to_latex import latex_to_png

path_data = os.path.join(Path.cwd(), '../data/')

data = pd.read_pickle(os.path.join(path_data, 'data.pkl'))

# We're including subjects with at least 55% performance
nsubjects = 66
include = np.where(np.array(100*data.groupby('subject').correct.mean().values, int) > 55)[0]
exclude = np.setdiff1d(range(nsubjects), include)
print(f"Subjects with performance < 0.55 (N={len(exclude)}, remain={nsubjects - len(exclude)}): [{', '.join([str(v) for v in exclude])}]")

map = dict(
    b_designated_absvaluediff='block_difficulty',
    b_valuebase='block_value_level',
    b_stimulus_pool='block_stimulus_type',
    b_ntrials_pre='block_ntrials_phase1',
    b_ntrials_noc='block_ntrials_phase2',
    absvaluediff='trial_difficulty',
    value_chosen='trial_value_chosen',
    trial_phase='trial_number',
    repeat_nr='trial_pair_repeat_nr',
)
d = data.copy().rename(columns=map)
ps = ['block_difficulty', 'block_value_level', 'block_stimulus_type',  'block_ntrials_phase1', 'block_ntrials_phase2', 'trial_difficulty', 'trial_value_chosen','trial_number', 'trial_pair_repeat_nr']
model = regression(
    d[~d.consistent.isna() & (d.phase == 1) & d.type_choice & ~d.subject.isin(exclude) & ~d.equal_value_pair],
    patsy_string='consistent ~ ' + ' + '.join(ps),
    standardize_vars=True,
    ignore_warnings=True,
    reml=False,
    print_data=False
)

latex_to_png(model, outpath=os.path.join(os.getcwd(), 'regtables', f'{Path(__file__).stem}.png'),
             title=None, DV='consistent')

# df = d[['consistent', 'subject', 'block'] + list(map.values())][~d.consistent.isna() & (d.phase == 1) & d.type_choice & ~d.subject.isin(exclude) & ~d.equal_value_pair]
# df.to_csv('data_phase2_consistency.csv')