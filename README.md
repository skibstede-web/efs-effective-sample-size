# EFS

This project develops a scientific framework for effective sample size in near-infrared (NIR) reflectance spectroscopy of powders.

The primary theoretical and simulation scaffold is in `notebooks/effective_sample_size_nir.ipynb`.

Implemented setup-specific notebooks:
- `notebooks/setup_A_static_effective_sample_size.ipynb` (Setup A: static powder bed)
- `notebooks/setup_B_spoon_effective_sample_size.ipynb` (Setup B: spoon-based repeated static sampling within one acquisition window)

Later setup notebooks and modeling modules may be added for Spoon, Spiderwheel, and Pipe, with optional modular code under `src/`.

The project uses SI units internally for all model calculations after input standardization.
