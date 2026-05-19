# Setup D Holdup-Adjusted Powder Flow and ESS Proxy Report

Setup: setup_d

Report timestamp: 20260512_085255

Source notebook: setup_D_pipe_effective_sample_size_holdup_refactor.ipynb

## Executive summary

Setup D now separates superficial velocity from holdup-adjusted local probe velocity and reports a one-spectrum ESS proxy as a near-wall renewal quantity. The total process mass crossing the axial location is reported separately to avoid conflating whole-stream throughput with the optical subset that contributes to one NIR spectrum.

## Key parameters

- Pipe diameter (mm): 65
- Pipe tilt from vertical (deg): 26.5
- Probe diameter (mm): 5
- Acquisition time (s): 1.8
- Mass flow (kg/h): 95
- Bulk density (g/cm^3): 0.4
- Nominal holdup fraction: 0.3
- Window coverage fraction: 1
- Wall velocity factor: 1
- Optical density factor: 1
- Holdup sensitivity values: 1, 0.6, 0.3, 0.15, 0.1, 0.05

## Background

Setup D represents an inclined powder-pipe geometry with a wall-mounted diffuse-reflectance NIR probe near the lower side of the pipe. Unlike the static bed in Setup A, the spoon presentations in Setup B, or the wheel-driven renewal in Setup C, this setup treats renewal as a flow-driven process in which fresh powder slides axially past a fixed probe during one acquisition.

The notebook uses a first-order engineering proxy to connect transport-side renewal with optical penetration depth. The reported quantity is a refresh-based proxy effective mass, intended for comparative sensitivity analysis and design-stage interpretation rather than as a validated independent sample mass.
## Objective

This notebook estimates, for Setup D:

- superficial velocity from mass balance
- apparent solids holdup at the probe location
- estimated local powder velocity near the NIR window
- renewal rate in front of the probe during one acquisition
- holdup-adjusted effective sample size proxy for one spectrum
- a separate convective swept-ribbon reference mass and the total process mass crossing the pipe section

The local velocity at the probe is not measured directly in this notebook. It is estimated from mass balance plus an apparent holdup assumption and treated as a sensitivity parameter.
## Theory

### Optical sampling concept

In diffuse reflectance NIR measurements, light enters a powder bed, interacts with particles over a limited depth, and a fraction of the scattered light returns to the detector. The measured spectrum therefore reflects an **optically weighted near-surface region** rather than the entire bulk stream.

For engineering comparisons, the instantaneous optical interaction region is approximated here as a simple cylinder with:

- cross-sectional area equal to the probe footprint
- depth equal to an assumed optical penetration depth

This simplification ignores depth-dependent photon weighting, scattering anisotropy, packing-dependent path-length effects, and spectral absorption details, but it provides a transparent basis for comparative analysis.

### Probe-flow geometry

In Setup D, the probe is mounted in the pipe wall and looks **radially inward**. The powder flows **axially** along the pipe. These directions are perpendicular.

At any instant, the probe sees a shallow optical disc of powder pressed against the wall:

- the disc face is the **probe footprint** with diameter $d_{\mathrm{probe}}$
- the disc depth is the **optical penetration depth** $d_{\mathrm{pen}}$ extending radially into the powder

Because the probe looks perpendicular to the flow, renewal occurs by material sliding **across** the probe window rather than being pushed **into** it. The flow supplies fresh material axially, while the light samples radially.

### Why a renewal model is appropriate

During one acquisition, the probe does not observe a single static neighborhood of powder. Instead, moving material repeatedly replaces the near-wall region in front of the probe. A renewal model is therefore a natural first-order way to connect powder motion to the mass that can contribute to one spectrum.

### Why superficial velocity is still useful

The notebook uses a **superficial bulk velocity** to estimate the renewal driver from throughput, bulk density, and full pipe cross-sectional area. This is a deliberate engineering approximation: the local wall velocity may differ from the cross-sectional average, but the superficial velocity still provides a transparent transport-side baseline for sensitivity analysis and model comparison.
## Velocity framework: superficial velocity, holdup, and local probe velocity

The mass flow gives a superficial velocity, $v_{sup}$, by dividing throughput by the product of flow bulk density and the full pipe cross-sectional area. This value is useful, but it is not automatically the velocity seen by the wall-mounted NIR probe.

In a completely filled pipe, $v_{sup}$ would equal the cross-sectional mean axial powder velocity. In a partially occupied gravity-flow pipe, the same mass flow passes through a smaller moving-powder area, so the occupied-region velocity is higher than the superficial velocity. The notebook represents this with an apparent cross-sectional solids holdup, $\phi_A$:

$$
v_{occ}=\frac{v_{sup}}{\phi_A}
$$

The probe-region velocity used for renewal is then:

$$
v_{probe}=k_{wall}\,\frac{v_{sup}}{\phi_A}
$$

Here $k_{wall}$ is an optional wall velocity factor. Values below 1 represent slower wall-adjacent powder; values above 1 represent a faster local stream intersecting the probe. The nominal model uses $\phi_A=0.30$ and $k_{wall}=1.0$, but $\phi_A$ is treated as a sensitivity parameter rather than a measured constant.
## Practical note on velocity estimation without high-speed imaging

The true local powder velocity at the NIR window is not measured in the present setup. The preferred evidence would be high-speed video, particle tracking, or a dedicated time-of-flight measurement close to the probe. Without those data, the notebook does not claim direct validation of $v_{probe}$.

Literature powder velocities are also not used as the primary basis for the calculation. Granular flow velocity depends strongly on powder properties, wall friction, aeration state, fill level, pipe geometry, and local flow regime, so a generic literature value would be hard to defend for this specific probe location.

The best available framework is therefore mass-balance based: known throughput defines $v_{sup}$, apparent holdup converts it to an occupied-region velocity, and the wall factor optionally adjusts that estimate at the NIR window. This makes the local velocity estimate explicit and auditable, while the holdup sensitivity table communicates the uncertainty caused by the missing direct velocity measurement.
## Assumptions

- Powder density used for the flow calculation represents the relevant dynamic bulk density unless otherwise specified.
- The NIR optical density is initially assumed equal to the flow bulk density.
- The nominal apparent holdup fraction is 0.30, based on visual engineering assessment.
- The actual holdup is uncertain and must be explored by sensitivity analysis.
- The nominal window coverage fraction is 1.0.
- The nominal wall velocity factor is 1.0.
- The model estimates an apparent local velocity, not a directly measured particle velocity.
- The ESS proxy describes near-wall material contributing to the NIR signal, not the full mass passing through the pipe.
## Input Parameters

Baseline geometry, acquisition settings, holdup assumptions, and sensitivity ranges are defined below. Engineering units are shown in the input block for readability, while calculations use consistent cm, g, and s units.

The baseline worked example uses:

- mass flow = 95 kg/h
- bulk density = 0.4 g/cm^3
- pipe diameter = 65 mm
- probe diameter = 5 mm
- penetration depth = 1.0 mm
- acquisition time = 1.8 s
- nominal apparent holdup fraction = 0.30
- nominal window coverage fraction = 1.0
- nominal wall velocity factor = 1.0
- optical density factor = 1.0
## Governing Equations and Proxy Definitions

Internal units used throughout the notebook are cm, g, and s. Reported outputs are shown in practical units (mm, mg, g, kg/h) as noted.

### Flow and velocity model

Mass-flow conversion:

$$
\dot{m}_{g/s} = \dot{m}_{kg/h}\cdot\frac{1000}{3600}
$$

Pipe area:

$$
A_{pipe} = \pi\left(\frac{d_{pipe}}{2}\right)^2
$$

Superficial velocity from mass balance:

$$
v_{sup} = \frac{\dot{m}}{\rho_{flow}\,A_{pipe}}
$$

Apparent occupied-region velocity:

$$
v_{occ} = \frac{v_{sup}}{\phi_A}
$$

Estimated local probe velocity with optional wall correction:

$$
v_{probe} = k_{wall}\,\frac{v_{sup}}{\phi_A}
$$

where $\phi_A$ is the apparent moving-powder holdup fraction, and $k_{wall}$ is an empirical wall-velocity factor.

### Optical mass and renewal

Optical density model:

$$
\rho_{opt} = \rho_{flow}\cdot f_{opt}
$$

Probe area:

$$
A_{probe} = \pi\left(\frac{d_{probe}}{2}\right)^2
$$

Instantaneous optical mass:

$$
m_{inst} = \rho_{opt}\,A_{probe}\,d_{pen}
$$

Renewal factor during one acquisition:

$$
N_{refresh} = \frac{v_{probe}\,t_{acq}\,C_{window}}{d_{probe}}
$$

Holdup-adjusted ESS proxy:

$$
m_{eff,proxy} = m_{inst}\,N_{refresh}
$$

Convective swept-ribbon reference mass (reported separately from ESS proxy):

$$
m_{swept} = \rho_{opt}\,A_{probe}\left(d_{pen}+v_{probe}\,t_{acq}\,C_{window}\right)
$$

Total process mass passing the full pipe cross-section during one acquisition:

$$
m_{process,total} = \dot{m}_{g/s}\,t_{acq}
$$

Interpretation boundary:

- $m_{process,total}$ is the total process mass crossing the axial location.
- The NIR signal represents only a near-wall optical subset of that process mass.
- Local velocity is estimated from mass balance and apparent holdup; it is not directly measured.
## Worked Example

Baseline worked example summary:

| Metric | Value | Unit |
| --- | --- | --- |
| mass flow | 95.0 | kg/h |
| bulk density | 0.4 | g/cm^3 |
| pipe diameter | 65.0 | mm |
| probe diameter | 5.0 | mm |
| penetration depth | 1.0 | mm |
| acquisition time | 1.8 | s |
| superficial velocity | 1.98813 | cm/s |
| apparent holdup fraction | 0.3 | - |
| wall velocity factor | 1.0 | - |
| window coverage fraction | 1.0 | - |
| estimated local probe velocity | 6.6271 | cm/s |
| travel distance during acquisition | 11.9288 | cm |
| instantaneous optical mass | 7.85398 | mg |
| renewal factor | 23.8575 | - |
| holdup-adjusted ESS proxy | 187.377 | mg |
| convective swept-ribbon reference mass | 0.944738 | g |
| total process mass passing pipe cross-section during acquisition | 47.5 | g |
## Holdup Sensitivity

Holdup sensitivity summary table:

| apparent_holdup_fraction | superficial_velocity_cm_s | local_probe_velocity_cm_s | travel_distance_cm | renewal_factor | ess_proxy_mg | convective_swept_ribbon_mass_g |
| --- | --- | --- | --- | --- | --- | --- |
| 1.0 | 1.9881 | 1.9881 | 3.5786 | 7.1573 | 56.213 | 0.2889 |
| 0.6 | 1.9881 | 3.3135 | 5.9644 | 11.9288 | 93.6884 | 0.4763 |
| 0.3 | 1.9881 | 6.6271 | 11.9288 | 23.8575 | 187.3767 | 0.9447 |
| 0.15 | 1.9881 | 13.2542 | 23.8575 | 47.7151 | 374.7535 | 1.8816 |
| 0.1 | 1.9881 | 19.8813 | 35.7863 | 71.5726 | 562.1302 | 2.8185 |
| 0.05 | 1.9881 | 39.7626 | 71.5726 | 143.1453 | 1124.2604 | 5.6292 |
## Figures

Figures progress from holdup-based velocity estimation to renewal and ESS consequences.

![Figure 1. Probe geometry and renewal bookkeeping schematic.](schematic_probe_geometry_and_bookkeeping.png)

![Figure 2. Estimated local probe velocity versus apparent holdup.](plot_01_local_velocity_vs_holdup.png)

![Figure 3. Renewal factor versus apparent holdup.](plot_02_renewal_vs_holdup.png)

![Figure 4. Holdup-adjusted ESS proxy versus apparent holdup.](plot_03_ess_proxy_vs_holdup.png)

![Figure 5. ESS proxy versus penetration depth for selected holdup values.](plot_04_ess_proxy_vs_penetration_selected_holdups.png)

![Figure 6. ESS proxy contour versus holdup and penetration depth.](plot_05_contour_ess_proxy_holdup_penetration.png)

![Figure 7. Baseline mass-scale comparison for one acquisition.](plot_06_mass_scale_comparison.png)
## Results Interpretation

The full-pipe superficial-velocity case should be interpreted as a conservative low-velocity reference. Lower apparent holdup values produce higher estimated local velocities because the same process mass flow is transported through a smaller occupied region of the pipe. As a result, powder renews more rapidly in front of the NIR window and the estimated one-spectrum ESS proxy increases approximately in proportion to 1/phi_A, provided optical density, window coverage, and wall velocity correction remain unchanged. The nominal 30% holdup case should therefore be viewed as a pragmatic engineering estimate, while the holdup sensitivity range communicates the uncertainty in the unmeasured local velocity.

For the baseline case, total process mass passing the full pipe cross-section during one 1.8 s spectrum is about 47.5 g, while the NIR proxy quantities are much smaller because they represent a near-wall optical subset.
## Limitations

- The local velocity at the NIR window is not directly measured.
- Apparent holdup is an assumed parameter informed by engineering judgment.
- Wall velocity factor and window coverage fraction are not independently measured in this notebook.
- The optical depth is modeled as a uniform effective penetration depth.
- The ESS quantity reported here is a mechanistic proxy for near-wall contributing mass, not a validated statistical ESS metric.
## Next Logical Extensions

Natural next steps for reducing model uncertainty are:

- acquire direct probe-region velocity evidence and use it to constrain $\phi_A$ and $k_{wall}$
- introduce intermittent coverage models where window coverage fraction falls below 1.0
- add uncertainty bands combining holdup, wall factor, and optical-density assumptions
- compare predicted ESS proxy trends against NIR spectral variance trends across throughput conditions
## Appendices

## Glossary of Variables and Symbols

| Symbol | Name | Meaning | Units |
|---|---|---|---|
| $\dot{m}$ | Mass flow | Process powder throughput | kg/h input; g/s internal |
| $\rho_{flow}$ | Flow bulk density | Dynamic bulk density used in mass-balance velocity estimate | g/cm^3 |
| $\rho_{opt}$ | Optical density | Optical-region density used for optical mass proxy | g/cm^3 |
| $A_{pipe}$ | Pipe area | Full internal pipe cross-sectional area | cm^2 |
| $A_{probe}$ | Probe area | Probe-window footprint area | cm^2 |
| $\phi_A$ | Apparent holdup fraction | Apparent fraction of cross-section occupied by moving powder | - |
| $v_{sup}$ | Superficial velocity | Mass-balance velocity based on full pipe area | cm/s |
| $v_{occ}$ | Occupied-region velocity | Velocity in the occupied moving region from holdup correction | cm/s |
| $v_{probe}$ | Estimated local probe velocity | Local velocity estimate after holdup and wall-factor correction | cm/s |
| $k_{wall}$ | Wall velocity factor | Empirical factor for wall-adjacent velocity vs occupied-region average | - |
| $C_{window}$ | Window coverage fraction | Fraction of acquisition time when probe window is covered by powder | - |
| $d_{probe}$ | Probe diameter | Probe-window diameter | mm input; cm internal |
| $d_{pen}$ | Optical penetration depth | Effective radial optical depth | mm input; cm internal |
| $t_{acq}$ | Acquisition time | One-spectrum acquisition duration | s |
| $m_{inst}$ | Instantaneous optical mass | Near-wall optical mass at one instant | g internal; mg reported |
| $N_{refresh}$ | Renewal factor | Effective number of probe-scale renewals during one spectrum | - |
| $m_{eff,proxy}$ | Holdup-adjusted ESS proxy | Renewal-adjusted optical proxy mass for one spectrum | g internal; mg reported |
| $m_{swept}$ | Convective swept-ribbon mass | Separate convective reference mass estimate near probe | g |
| $m_{process,total}$ | Total process mass during acquisition | Mass crossing full pipe section during one spectrum | g |
## Renewal-Based ESS Versus Subscan Multiplication

### Question: Is effective sample size just static optical mass times number of subscans?

For a 1.8 s NIR spectrum built from 150 subscans at 12 ms each, a tempting shortcut is:

$$
m_{ESS,naive}=m_{static}\,N_{subscan}
$$

If a static optical mass is assumed to be 12 mg, this gives:

$$
12\;\mathrm{mg}\times150=1800\;\mathrm{mg}
$$

This is a detector-counting calculation, not a powder-renewal calculation. It assumes that each electronic subscan sees a fresh, non-overlapping powder volume. That assumption is not supported by the Setup D velocity framework.

### Developed model used in this notebook

The holdup-adjusted model separates three quantities that the naive shortcut collapses into one number:

1. instantaneous optical mass at the NIR window
2. powder velocity at the probe estimated from mass balance and apparent holdup
3. renewal count during the 1.8 s acquisition

The model estimate is:

$$
m_{ESS,proxy}=m_{inst}\,N_{refresh}
$$

with:

$$
N_{refresh}=\frac{v_{probe}\,t_{acq}\,C_{window}}{d_{probe}}
$$

and:

$$
v_{probe}=k_{wall}\,\frac{v_{sup}}{\phi_A}
$$

Thus the multiplier is not the number of electronic subscans. The multiplier is the number of probe-diameter-scale powder renewals, and that multiplier depends directly on apparent holdup fraction, wall velocity factor, and window coverage.

### Baseline comparison

For the baseline case in this notebook:

- superficial velocity is about 1.99 cm/s
- nominal apparent holdup is 0.30
- estimated local probe velocity is about 6.63 cm/s
- powder advances about 0.80 mm during one 12 ms subscan
- one probe diameter is 5 mm

So one subscan advances the powder by only about 16% of a probe diameter. Consecutive subscans therefore overlap strongly in space and cannot be counted as 150 independent static samples.

The notebook's geometric optical-mass model gives:

$$
m_{inst}=\rho_{opt}\,A_{probe}\,d_{pen}\approx7.85\;\mathrm{mg}
$$

The nominal holdup-adjusted renewal count is:

$$
N_{refresh}\approx23.9
$$

Therefore:

$$
m_{ESS,proxy}\approx7.85\;\mathrm{mg}\times23.9\approx187\;\mathrm{mg}
$$

If an external static-scan estimate of 12 mg is used as the instantaneous optical mass instead, the same developed renewal logic would give:

$$
12\;\mathrm{mg}\times23.9\approx286\;\mathrm{mg}
$$

not 1800 mg. The difference is the multiplier: the physically relevant multiplier is powder renewal, not detector subscan count.

### Holdup sensitivity of the comparison

The naive 1800 mg estimate is independent of flow geometry. The developed model is not; it changes with apparent occupied fraction in the pipe.

| Apparent holdup $\phi_A$ | Estimated $v_{probe}$ (cm/s) | Powder advance per subscan (mm) | Renewal factor | ESS proxy using notebook $m_{inst}$ (mg) | Naive 1800 mg / model |
|---:|---:|---:|---:|---:|---:|
| 1.00 | 1.99 | 0.24 | 7.16 | 56 | 32.0x |
| 0.60 | 3.31 | 0.40 | 11.93 | 94 | 19.2x |
| 0.30 | 6.63 | 0.80 | 23.86 | 187 | 9.6x |
| 0.15 | 13.25 | 1.59 | 47.72 | 375 | 4.8x |
| 0.10 | 19.88 | 2.39 | 71.57 | 562 | 3.2x |
| 0.05 | 39.76 | 4.77 | 143.15 | 1124 | 1.6x |

This table shows why the apparent holdup framework matters. Lower holdup means the same mass flow is carried through a smaller occupied region, so the estimated local velocity and renewal count increase. Even then, the naive 150-subscan multiplier is only approached near the extreme low-holdup end of the sensitivity range.

### What holdup would make the naive multiplier plausible?

For every 12 ms subscan to see a full new probe footprint, the probe-region velocity would need to be:

$$
v_{required}=\frac{d_{probe}}{t_{subscan}}=\frac{0.5\;\mathrm{cm}}{0.012\;\mathrm{s}}=41.67\;\mathrm{cm/s}
$$

Using the baseline superficial velocity and $k_{wall}=1$, this corresponds to:

$$
\phi_A\approx\frac{v_{sup}}{v_{required}}\approx\frac{1.99}{41.67}\approx0.048
$$

That is an extreme apparent occupied fraction, close to the 0.05 sensitivity case and far below the nominal 0.30 engineering estimate. It should not be assumed unless supported by direct evidence such as high-speed imaging, particle tracking, or local time-of-flight data.

### Conclusion

The naive calculation can be useful as a reminder of the detector timing, but it is not a physically consistent ESS estimate for Setup D. In the developed model, ESS is controlled by near-wall optical mass and powder renewal:

$$
m_{ESS,proxy}=m_{inst}\left(\frac{k_{wall}\,v_{sup}\,t_{acq}\,C_{window}}{\phi_A\,d_{probe}}\right)
$$

The subscan count does not become a powder-renewal count unless the powder actually moves about one probe diameter per subscan. For the nominal 30% holdup case, it does not.
## Exported artifacts

CSV files

- worked_example_summary.csv
- holdup_sensitivity.csv
- penetration_sweep.csv
- mass_scale_comparison.csv

Figure files

- schematic_probe_geometry_and_bookkeeping.png
- plot_01_local_velocity_vs_holdup.png
- plot_02_renewal_vs_holdup.png
- plot_03_ess_proxy_vs_holdup.png
- plot_04_ess_proxy_vs_penetration_selected_holdups.png
- plot_05_contour_ess_proxy_holdup_penetration.png
- plot_06_mass_scale_comparison.png
