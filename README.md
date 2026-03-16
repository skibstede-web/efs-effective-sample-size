git diff# Effective Sample Size (EFS) for NIR Powder Analysis

## Summary
This repository contains simulation notebooks, configuration templates, and supporting Python utilities for reasoning about effective sample size (EFS) in near-infrared (NIR) analysis of powders. In this context, effective sample size refers to the amount of material that meaningfully contributes to the measured optical signal during a given acquisition, rather than the total mass physically present in the broader process environment.

For diffuse reflectance or related NIR powder measurements, the instrument does not interrogate all available material equally. The sampled region depends on optical penetration depth, illuminated area, presentation geometry, powder packing, and whether material is static, intermittently presented, or continuously refreshed by motion. These distinctions matter when comparing sampling arrangements, interpreting measurement robustness, or designing experiments for process analytical technology (PAT) and chemometric development.

## Scientific Motivation
In powder spectroscopy, measurement quality is strongly linked to how representative the optically interrogated material is of the bulk. A nominally large vessel, pipe, or sampler may still present only a limited effective mass to the instrument at any instant. Conversely, a moving stream can refresh the optical sampling volume repeatedly during an acquisition window, potentially increasing the amount of distinct material observed over time.

This makes effective sample size a useful mechanistic concept for PAT scientists, chemometricians, and process engineers. It helps connect instrument geometry and process conditions to practical questions such as:

- whether a sampling arrangement is likely to average over enough material heterogeneity
- how strongly setup design influences measurement representativeness
- when a static interface behaves differently from a dynamically refreshed one
- which parameters are most worth measuring, controlling, or sweeping during design studies

Several physical and operational factors can influence the mass effectively interrogated by an NIR measurement, including:

- probe or window diameter and illuminated footprint
- optical penetration depth into the powder bed
- bulk density and local packing structure
- particle motion, replenishment, or residence time in the measurement zone
- acquisition time and scan averaging strategy
- intermittent versus continuous sample presentation
- geometric constraints such as spoon cavities, rotating hardware, or pipe cross-sections

Simulation is valuable here because it provides a structured way to test assumptions before building or modifying experimental hardware. Mechanistic notebook studies can help frame design decisions, identify dominant sensitivities, and support more focused experimental campaigns. They are especially useful when multiple candidate geometries are under consideration and a full physical test program would be time-consuming or expensive.

## Project Objectives
- Compare alternative powder presentation and sampling geometries in terms of likely effective sample size behavior.
- Support mechanistic understanding of how NIR optics and powder motion interact.
- Provide notebook-based scenario exploration for setup-specific studies.
- Create a reusable structure for parameters, units, and reporting outputs.
- Help organize future design, qualification, and method-development discussions.
- Enable reproducible generation of summary tables, figures, metadata, and report artifacts.

## Repository Structure
The repository currently contains notebooks, configurations, utilities, generated reports, and output folders. A simplified structure based on the local workspace is shown below.

```text
EFS/
+-- README.md
+-- .gitignore
+-- configs/
|   +-- parameter_registry_template.json
|   +-- unit_conventions.md
+-- notebooks/
|   +-- effective_sample_size_nir.ipynb
|   +-- setup_A_static_effective_sample_size.ipynb
|   +-- setup_B_spoon_effective_sample_size.ipynb
|   +-- setup_C_spiderwheel_effective_sample_size.ipynb
|   +-- setup_D_pipe_effective_sample_size.ipynb
|   +-- spiderwheel.ipynb
|   +-- selected exported CSV result files
+-- reports/
|   +-- setup_a/
|   +-- setup_b/
|   +-- setup_c/
|   +-- setup_d/
+-- results/
|   +-- figures/
|   +-- tables/
|   +-- selected exported result files
+-- requirements/
+-- references/
+-- src/
    +-- reporting_utils.py
```

### Folder and file roles
- `notebooks/`: Primary analysis and simulation workspace. This includes setup-specific notebooks and at least one broader scaffold notebook, `effective_sample_size_nir.ipynb`.
- `configs/`: Parameter and unit-management material intended to support consistency across studies.
- `src/`: Reusable Python code, currently including utilities for exporting figures, tables, metadata, and Word reports from notebook runs.
- `reports/`: Timestamped run outputs organized by setup, including CSV summaries, PNG figures, metadata, and generated `.docx` reports.
- `results/`: Additional exported results and output artifacts.
- `requirements/`: Reserved location for dependency specifications or environment-related files if maintained separately.
- `references/`: Reserved space for supporting background material or project references.

## Simulation Setups
The notebook naming strongly suggests that the repository is organized around distinct physical sample-presentation scenarios. The descriptions below are careful interpretations of the local file structure and naming, not claims about fully validated implementations.

### Setup A: Static Powder Interface
Notebook: `notebooks/setup_A_static_effective_sample_size.ipynb`

This setup appears to represent a static powder bed or stationary powder interface measured through a fixed optical footprint. In this scenario, the effective sample size is likely governed primarily by geometric and optical factors rather than by material refresh through motion.

Parameters that may matter in this type of model include:

- penetration depth into the powder bed
- probe diameter, window diameter, or illumination diameter
- interaction area or interaction volume assumptions
- powder bulk density
- assumptions about uniformity within the sampled volume

Questions this setup can support include:

- how effective sampled mass changes with penetration depth
- how density influences the relationship between sampled volume and sampled mass
- what static mass is plausibly interrogated by a given optical footprint
- whether a static interface is likely to be representative for a heterogeneous powder

### Setup B: Spoon-Based Intermittent Sampling
Notebook: `notebooks/setup_B_spoon_effective_sample_size.ipynb`

This setup appears to represent powder being presented intermittently via spoons or spoon-like compartments. The measurement may involve repeated presentation of discrete powder volumes into the optical path over one acquisition period or across repeated intervals.

Parameters that may matter include:

- spoon geometry or cavity volume
- the amount of static mass presented per spoon event
- interval between presentations or flips
- acquisition duration relative to presentation frequency
- penetration depth and optical footprint within each presented spoon sample
- the number of discrete spoon presentations contributing to one effective measurement window

Questions this setup can support include:

- how much static mass is sampled per spoon event
- how presentation interval affects cumulative effective sampled mass
- when the setup behaves more like repeated discrete sampling versus quasi-continuous refresh
- how many spoons may contribute during an acquisition period

The presence of exported outputs such as `plot_04_effective_sample_size_vs_flip_interval.png` and related CSV files suggests this setup is already used for interval-based scenario analysis.

### Setup C: Spiderwheel Sampling
Notebook: `notebooks/setup_C_spiderwheel_effective_sample_size.ipynb`

This setup appears to model a rotating spiderwheel-style sampler or a mechanically indexed presentation device in which powder periodically enters and leaves the optical measurement region. Relative to the spoon setup, the spiderwheel case may place more emphasis on rotational speed, dwell time, blockage fraction, and repeated refreshing of the optical zone.

Parameters that may matter include:

- wheel rotational speed or RPM
- number and geometry of compartments or sampling features
- blocked versus exposed measurement time
- powder mass delivered or exposed per refresh event
- acquisition time relative to wheel rotation dynamics
- penetration depth, density, and footprint assumptions

Questions this setup can support include:

- how effective sample size scales with rotational speed
- whether the instrument is material-limited or refresh-limited
- how blocked time or duty cycle affects usable sampling
- how optical mass per refresh varies with geometry and penetration depth

The existing report outputs indicate that this setup likely includes summaries of blocked time fraction, optical mass per refresh, and parameter sweeps across rotational conditions.

### Setup D: Flowing Powder in a Pipe
Notebook: `notebooks/setup_D_pipe_effective_sample_size.ipynb`

This setup appears to address in-line or at-line measurement of powder flowing through a pipe. In such a case, effective sample size is not only a static volume concept; it also depends on how much distinct material passes through the measurement footprint during the acquisition time.

Parameters that may matter include:

- pipe diameter
- mass flow rate
- superficial or effective flow velocity
- filled fraction
- velocity profile assumptions
- wall stagnation or non-ideal flow factors
- acquisition time and scan averaging
- penetration depth and interaction area
- bulk density

Questions this setup can support include:

- how much material passes through the optical sampling zone during a measurement
- how throughput and velocity change the refreshed mass available to the instrument
- when the effective sample size is dominated by optical penetration versus process flow
- how density and fill assumptions alter the relationship between mass flow and observed mass

The local parameter template explicitly contains a `pipe` section with fields such as `pipe_diameter_m`, `mass_flow_rate_kg_s`, `velocity_profile_factor`, and `filled_fraction`, which supports this interpretation.

### `spiderwheel.ipynb`
Notebook: `notebooks/spiderwheel.ipynb`

This notebook likely serves as an exploratory, developmental, or supporting notebook related to the spiderwheel concept. It may contain intermediate derivations, prototype calculations, or visual checks that complement the more formal setup-specific notebook. Users should review it as supporting analysis unless its scope and purpose are made explicit inside the notebook itself.

### General Scaffold Notebook
Notebook: `notebooks/effective_sample_size_nir.ipynb`

Based on its name, this notebook appears to provide broader theoretical or conceptual scaffolding for the repository. It is a reasonable starting point for understanding the modeling approach before diving into individual geometries.

## Key Concepts and Model Inputs
The repository likely uses several common physical concepts across setups. The items below are framed as conceptual inputs and modeling dimensions inferred from the local files and parameter templates.

### Effective Sample Size
Effective sample size is the amount of powder that contributes meaningfully to the measured NIR signal over the relevant measurement period. Depending on setup, this may correspond to:

- a static optically sampled mass
- a cumulative refreshed mass over time
- a proxy quantity linked to representativeness rather than a directly observable mass

### Penetration Depth
Penetration depth represents the characteristic depth over which photons meaningfully interact with the powder. It is a central parameter because it helps translate illuminated area into sampled volume. In practice, this quantity may be treated as an assumed or scenario-swept input rather than a precisely known constant.

### Probe or Window Diameter
The illuminated spot size, probe diameter, or viewing window diameter helps define the lateral extent of the optical interaction region. Together with penetration depth and geometry factors, it influences the estimated sampled volume.

### Bulk Density
Bulk density is needed to convert sampled volume into sampled mass. For powders, density can vary with packing, aeration, consolidation, and flow state, so sensitivity to this parameter is often important.

### Flow Velocity and Throughput
In dynamic systems such as pipe flow or rotating samplers, velocity and throughput influence how quickly the optically sampled region is refreshed. These quantities are essential when moving from a static sampled mass concept to a time-integrated effective sampled mass.

### Spectral Acquisition Time
Acquisition time determines how long the system observes a static or moving powder population. For dynamic measurements, the total amount of distinct material sampled can change substantially as acquisition time increases.

### Intermittent Versus Continuous Presentation
Some geometries appear to present material in discrete packets or exposure events, while others behave more continuously. This distinction affects whether the effective sample size scales in steps, through periodic refresh, or through continuous passage of mass through the optical zone.

### Static Mass Versus Passed Mass
A useful conceptual distinction is the difference between:

- the mass contained inside the optical interaction volume at any moment
- the total mass that passes through that interaction volume during an acquisition window

Both can matter, but they are not interchangeable. Their relative importance depends on geometry, motion, and the assumptions of the measurement model.

## Project Files and Supporting Utilities

### `src/reporting_utils.py`
This module provides reusable export and reporting functions for notebook workflows. Based on the local source code, it supports:

- creating timestamped run directories under `reports/`
- saving pandas DataFrames as CSV files
- saving matplotlib figures as PNG files
- writing metadata as JSON
- extracting markdown narrative from notebooks
- rendering notebook markdown and figures into Word reports

This is useful for turning exploratory notebook work into traceable output packages that can be shared with collaborators or retained as run records.

### `configs/parameter_registry_template.json`
This file provides a structured template for model inputs and assumptions. It includes sections for:

- metadata
- powder properties
- optics
- acquisition settings
- assumptions
- setup-specific fields
- sweep definitions

This kind of registry is useful for reproducibility because it encourages explicit parameter declaration and clearer separation between scenario inputs and derived outputs.

### `configs/unit_conventions.md`
This document defines internal SI unit expectations and naming conventions such as `parameter_name_unit`. It also states that all user-facing inputs should be standardized to SI units before calculations and that derived quantities should be stored separately from raw inputs.

For a scientific modeling repository, these conventions are important because they reduce ambiguity, improve comparability between notebooks, and lower the risk of silent unit conversion errors.

## How to Use This Repository
The repository appears to be designed for notebook-driven scientific exploration in a Python environment. The exact dependency installation method may evolve over time, especially if environment files are added later under `requirements/` or elsewhere. A practical starting workflow in VS Code is shown below.

### 1. Clone the repository
```powershell
git clone <repository-url>
cd EFS
```

### 2. Create a virtual environment
```powershell
python -m venv .venv
```

### 3. Activate the environment in PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies
If a `requirements.txt`, environment file, or setup instructions are later added, adapt the installation step to match the repository's actual dependency specification. For example:

```powershell
pip install -r requirements.txt
```

If no single dependency file is present, install the packages required by the notebooks and utilities in your local workflow. Based on the current source code, packages such as `pandas`, `matplotlib`, `nbformat`, and `python-docx` may be relevant for some notebook export paths.

### 5. Open the repository in VS Code
Open the project folder in VS Code and ensure the selected Python interpreter points to `.venv`.

### 6. Open and run notebooks
Start with:

- `notebooks/effective_sample_size_nir.ipynb` for general context
- one of the setup notebooks for a geometry-specific study

Run cells interactively in VS Code or in Jupyter, review outputs, and inspect any generated files under `reports/` or `results/`.

## Suggested Workflow
- Read this `README.md` to understand repository scope and intent.
- Review `configs/unit_conventions.md` before changing or adding parameters.
- Inspect `configs/parameter_registry_template.json` to understand the expected structure for scenario inputs.
- Start with `notebooks/effective_sample_size_nir.ipynb` if you want conceptual context.
- Open one setup notebook corresponding to the geometry of interest.
- Review notebook assumptions, units, and sweep definitions before running simulations.
- Run scenario calculations and compare how the predicted effective sample size changes with geometry and process conditions.
- Save or review generated figures, CSV tables, metadata, and reports under `reports/` and `results/`.
- Document conclusions carefully as model-based observations unless supported by independent experimental evidence.

## Current Scope and Limitations
This repository should be treated as a simulation and analytical support environment, not as stand-alone proof of measurement performance. Important limitations likely include:

- geometric simplifications relative to real hardware and powder behavior
- dependence on assumed inputs such as penetration depth, density, or flow factors
- possible use of idealized models such as plug flow, uniform penetration, or simplified refresh assumptions
- sensitivity to acquisition timing and presentation assumptions
- incomplete linkage, within the repository itself, to formal experimental validation data

Accordingly:

- results should be interpreted as model-based support for reasoning and design
- conclusions may be scenario-dependent and parameter-dependent
- repository outputs should not be treated as regulatory evidence by themselves
- any design or method decision informed by these models should be checked against experimental and process knowledge

## Potential Future Extensions
- Link the simulation framework to experimental qualification or calibration-support datasets.
- Add uncertainty propagation and formal sensitivity analysis.
- Expand treatment of non-ideal flow, segregation, residence time distributions, or stochastic presentation effects.
- Introduce additional geometries or probe configurations.
- Add more explicit parameter schemas and validation utilities.
- Integrate notebook outputs more tightly with automated reporting pipelines.
- Connect the mechanistic modeling workflow to chemometric method-development decisions such as averaging strategy, sampling strategy, or representativeness assessments.

## Recommended Citation / Usage Note
Until a formal publication or internal report series is established, users should cite the GitHub repository itself when using this material in internal documentation, presentations, or external work. Where possible, include the repository name, access date, and the specific version tag or commit hash used for the analysis.

## Author / Maintainer
Maintainer information can be added here as the project matures.

Suggested format:

- Maintainer: `<name>`
- Organization or group: `<team / department / company>`
- Contact: `<email or repository contact path>`
