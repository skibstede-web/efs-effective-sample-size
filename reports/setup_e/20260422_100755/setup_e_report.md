# Setup E PAT Rig Swept-Capsule Effective Sample Size Report

Setup: setup_e

Report timestamp: 20260422_100755

Source notebook: setup_E_PATrig_effective_sample_size.ipynb

## Executive summary

Setup E treats the PAT rig as a covered-probe vertical sampling interface in which powder continuously moves past a side-window non-contact NIR measurement location. The primary effective sample size is now the unique exposed optical mass represented by the initial circular 25 mm NIR footprint plus the swept capsule extension created by powder motion during acquisition. The report also retains instantaneous probed mass, swept-in incremental mass, mass-passed diagnostics, and a simple time-weighted contribution proxy for future research.

## Key parameters

- Pipe diameter (cm): 10
- NIR spot diameter (cm): 2.5
- Base measurement depth (cm): 0.1
- Measurement depth sweep (mm): 0.1 to 2.0
- Bulk density scenarios (g/cm^3): 0.4, 0.5, 0.6
- Base throughput (kg/h): 95
- Acquisition time sweep (s): 1.0 to 5.0
- Throughput sweep (kg/h): 10 to 100
- Primary ESS proxy: unique exposed swept capsule mass

## Background

Setup E models a PAT (Process Analytical Technology) rig as a vertical cylindrical sampling interface fed continuously from an upstream manufacturing unit. A rotating outlet valve at the bottom controls discharge, while level sensors along the wall maintain the rig at approximately half full during operation.

The primary NIR instrument views the powder through a side optical window positioned near the lower part of the rig. In the base case used here, the measurement location is one-quarter of the rig height above the bottom outlet and the non-contact NIR spot diameter is 25 mm.

At the start of a spectral acquisition, all powder inside the circular NIR footprint contributes to the measured spectrum. During the acquisition, powder motion translates new material into the beam. Because the Setup E NIR spot is large relative to the powder advance during a 1 s acquisition, the effective sample size should include both the initial circular footprint and the additional swept-in material. The primary proxy in this notebook therefore represents the unique exposed powder as a rounded-end capsule footprint multiplied by optical penetration depth.
## Objective

Compute three Setup E sampling quantities:

1. instantaneous probed mass at acquisition start
2. unique exposed effective sample size using swept capsule geometry
3. time-weighted contribution proxy retained as a future research quantity

The analysis sweeps bulk density, penetration depth, acquisition time, and throughput while keeping the covered-probe PAT rig geometry and 25 mm NIR spot fixed.
## Theory

### Covered-Probe PAT Rig Geometry

The PAT rig is represented as a vertical cylindrical flow region observed through a side optical window. The operating assumption is that level control keeps the probe window buried in powder during normal operation, so probe coverage is treated as guaranteed.

### Throughput-Derived Powder Velocity

Powder motion near the covered probe is approximated as a first-order dense moving column. The local axial velocity is estimated from throughput and the full cylindrical cross-section:

$$
v = \frac{\dot{m}}{\rho_{bulk} \cdot A_{pipe}}
$$

where

$$
A_{pipe} = \pi \left(\frac{D_{pipe}}{2}\right)^2
$$

This is a simplifying assumption. It ignores wall slip, local recirculation, outlet-valve kinematics, and nonuniform velocity profiles near the probe.

### Quantity 1: Instantaneous Probed Mass

The non-contact NIR spot is represented as a circular optical footprint:

$$
A_{spot} = \pi \left(\frac{D_{spot}}{2}\right)^2
$$

The instantaneous probed mass at acquisition start is:

$$
m_{inst} = \rho_{bulk} \cdot A_{spot} \cdot d_{pen}
$$

### Quantity 2: Unique Exposed Effective Sample Size

During an acquisition of length $T_{acq}$, powder advances by:

$$
\Delta z = v \cdot T_{acq}
$$

The unique footprint exposed at least once is approximated as a swept capsule: the initial circular spot plus a rectangular swept increment of width $D_{spot}$ and length $\Delta z$:

$$
A_{unique} = A_{spot} + D_{spot} \cdot \Delta z
$$

The primary effective sample size proxy is therefore:

$$
m_{unique} = \rho_{bulk} \cdot A_{unique} \cdot d_{pen}
$$

This proxy counts unique material exposed at least once. It does not weight by residence time or optical intensity.

### Quantity 3: Time-Weighted Contribution Proxy

A measured NIR spectrum is time-integrated, so material that remains in the beam longer can contribute more strongly than material briefly entering near an edge. This notebook retains a simple mass-time proxy:

$$
m_{time} = m_{inst} \cdot T_{acq}
$$

This is retained for future research only. It is not the primary effective sample size in this notebook.

### Related Diagnostic: Mass Passed the NIR Footprint

The mass passed diagnostic is:

$$
m_{pass} = \rho_{bulk} \cdot A_{spot} \cdot v \cdot T_{acq}
$$

This quantity is useful as a transport reference, but it should not be interpreted as the optical effective sample size because it does not include penetration-depth reduction.
## Interpreting Density, Velocity, and Throughput

At fixed mass throughput, the local powder velocity in this model is inversely proportional to bulk density:

$$
v = \frac{\dot{m}}{\rho_{bulk} \cdot A_{pipe}}
$$

For the same throughput and PAT rig cross-section, lower bulk-density powder occupies a larger volumetric flow rate and therefore moves faster past the probe. Higher bulk-density powder moves more slowly.

This has two consequences in the capsule model:

1. Increasing bulk density increases the instantaneous mass in the initial circular NIR footprint.
2. Increasing bulk density decreases the powder advance during acquisition, which reduces the swept-in incremental contribution.

Unlike a pure renewal-count proxy, density does not fully cancel in the primary Setup E effective sample size because the initial circular footprint is always included.
## Three Sampling Quantities Used in This Notebook

This notebook separates three related but distinct quantities:

1. **Instantaneous probed mass**: material inside the circular NIR footprint at acquisition start.
2. **Unique exposed effective sample size**: all material exposed at least once during acquisition, represented by the swept capsule footprint.
3. **Time-weighted contribution proxy**: a simple mass-time exposure proxy retained for future research.

The unique exposed effective sample size is the primary reported ESS in this notebook. The time-weighted proxy should not be interpreted as the primary ESS.
## Assumptions

- vertical cylindrical PAT rig with top feed and bottom discharge through a rotating outlet valve
- the operating window is controlled so the probe window remains continuously covered during normal operation
- no explicit level-control dynamics are modeled because probe coverage is treated as guaranteed by design
- the powder near the probe is treated as a dense moving column
- powder velocity at the probe is approximated from throughput and full pipe cross-section
- the NIR spot is circular and viewed through a side optical window
- powder motion during one acquisition is represented as linear translation across the spot
- the unique exposed footprint is represented as a swept capsule: initial circle plus rectangular extension
- measurement depth is uniform over the full exposed capsule footprint
- the capsule model counts material exposed at least once, regardless of how long it remains inside the beam
- no explicit outlet-valve kinematics, turbulence, segregation, recirculation, or wall-slip correction
- no detailed radiative-transfer model or optical intensity weighting is included
## Compute Sampling Metrics

Run a discrete bulk-density comparison together with a penetration-depth sweep by density, an acquisition-time sweep by density, and a throughput-acquisition-time sweep by density. The primary effective sample size is the unique exposed mass from the swept capsule footprint.
## Worked example

The baseline case reports the center density scenario, base-case penetration depth, powder advance during one acquisition, instantaneous circular mass, swept-in incremental mass, unique exposed capsule mass, the resulting primary effective sample size, the transport mass-passed diagnostic, and the future-research time-weighted proxy.

| Quantity | Value |
| --- | --- |
| bulk_density_g_per_cm3 | 0.5 |
| measurement_depth_cm | 0.1 |
| measurement_depth_mm | 1 |
| nir_spot_diameter_cm | 2.5 |
| velocity_mm_s | 6.71988 |
| acquisition_time_s | 1 |
| advance_dz_mm_per_acq | 6.71988 |
| probe_mass_mg_instant | 245.437 |
| swept_increment_mass_mg | 83.9984 |
| unique_exposed_mass_mg | 329.435 |
| effective_sample_size_mg | 329.435 |
| mass_passed_mg_per_acq | 1649.31 |
| time_weighted_contribution_proxy_mg_s | 245.437 |
## Model scenarios and sweep design

The Setup E analysis combines a discrete bulk-density comparison with a penetration-depth sweep by density, an acquisition-time sweep by density, and a throughput-by-acquisition-time sweep by density. The primary response is the swept-capsule unique exposed mass.

- bulk density scenarios: 0.4, 0.5, and 0.6 g/cm^3
- penetration depth swept from 0.1 to 2.0 mm in 0.1 mm steps for each density
- acquisition time swept from 1.0 to 5.0 s for each density
- throughput swept from 10 to 100 kg/h for each density
- NIR spot diameter fixed at 2.5 cm

This produces 1323 modeled rows across the density-aware sweeps.
## Selected results table

The selected table compares the three bulk-density scenarios at the common base operating condition. It separates instantaneous circular mass, swept-in incremental mass, unique exposed mass, and the final primary ESS.

| bulk_density_g_per_cm3 | velocity_mm_s | acquisition_time_s | advance_dz_mm_per_acq | probe_mass_mg_instant | swept_increment_mass_mg | unique_exposed_mass_mg | effective_sample_size_mg | mass_passed_mg_per_acq | time_weighted_contribution_proxy_mg_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.4000 | 8.3998 | 1.0000 | 8.3998 | 196.3495 | 83.9984 | 280.3480 | 280.3480 | 1649.3056 | 196.3495 |
| 0.5000 | 6.7199 | 1.0000 | 6.7199 | 245.4369 | 83.9984 | 329.4354 | 329.4354 | 1649.3056 | 245.4369 |
| 0.6000 | 5.5999 | 1.0000 | 5.5999 | 294.5243 | 83.9984 | 378.5228 | 378.5228 | 1649.3056 | 294.5243 |
## Figures

The figures are ordered from the geometric decomposition of effective sample size to penetration-depth trends, powder-advance behavior, operating maps, the future-research time-weighted proxy, and the capsule schematic.

![Figure 1. Instantaneous circular mass, swept-in incremental mass, and unique exposed ESS versus penetration depth for the base density case.](plot_01_instant_swept_unique_vs_penetration_depth.png)

![Figure 2. Swept-capsule effective sample size versus penetration depth for bulk densities of 0.4, 0.5, and 0.6 g/cm^3.](plot_02_effective_sample_size_vs_penetration_depth_by_density.png)

![Figure 3. Powder advance during acquisition versus acquisition time for the three bulk-density scenarios.](plot_03_powder_advance_vs_acquisition_time.png)

![Figure 4. Swept-capsule effective sample size versus acquisition time for the three bulk-density scenarios.](plot_04_effective_sample_size_vs_acquisition_time_by_density.png)

![Figure 5. Swept-in incremental mass versus acquisition time for the three bulk-density scenarios.](plot_05_swept_increment_mass_vs_acquisition_time_by_density.png)

![Figure 6. Throughput-acquisition heatmap for swept-capsule effective sample size at 0.4 g/cm^3 bulk density.](plot_06_heatmap_effective_sample_size_density_04.png)

![Figure 7. Throughput-acquisition heatmap for swept-capsule effective sample size at 0.5 g/cm^3 bulk density.](plot_07_heatmap_effective_sample_size_density_05.png)

![Figure 8. Throughput-acquisition heatmap for swept-capsule effective sample size at 0.6 g/cm^3 bulk density.](plot_08_heatmap_effective_sample_size_density_06.png)

![Figure 9. Time-weighted contribution proxy versus acquisition time, retained as a future-research quantity rather than the primary ESS.](plot_09_time_weighted_proxy_vs_acquisition_time_by_density.png)

![Figure 10. Schematic of the swept capsule geometry used for the primary unique exposed effective sample size proxy.](schematic_swept_capsule_geometry.png)
## Results Interpretation

- The primary effective sample size now includes all material exposed at least once during acquisition.
- The base case contains the full initial circular spot plus an additional swept-in strip generated by powder motion during the 1 s acquisition.
- Because the 25 mm spot is large relative to the base-case powder advance, the instantaneous component remains a major part of the effective sample size.
- Increasing acquisition time increases effective sample size by elongating the exposed capsule footprint.
- Increasing penetration depth increases instantaneous mass, swept-in incremental mass, and effective sample size linearly.
- Lower bulk density increases powder velocity and the swept increment at fixed throughput, while higher bulk density increases the mass in the initial circular footprint.
- The time-weighted contribution proxy is retained only as a future route toward residence-time and optical-weighting analysis.
## Practical Implications

- Large NIR spots at low powder velocity should not use a refresh-fraction-only effective sample size proxy.
- The starting circular footprint can dominate the effective sample size when powder advance is small relative to spot diameter.
- Acquisition time elongates the exposed footprint rather than simply replacing a fraction of the original spot.
- For Setup E, the swept capsule model better matches the all-unique-exposed-material logic used elsewhere in the project.
- Throughput directly controls powder advance and therefore the incremental swept contribution, but the initial circular contribution remains present for every spectrum.
## Limitations

- probe coverage is assumed guaranteed and is not stress-tested against abnormal operating states
- the rotating outlet valve is not modeled dynamically
- the local velocity near the probe is approximated from throughput and full pipe cross-section
- straight-line translation of powder past the spot is assumed
- velocity is assumed uniform over the NIR spot footprint
- penetration depth is uniform over the full capsule footprint
- residence-time differences across the swept capsule are not included in the primary ESS
- radial and tangential optical intensity gradients are ignored
- penetration depth is swept as an effective parameter, not derived from a wavelength-dependent optical model
- bulk density is treated as spatially uniform and fixed within each scenario
- no particle-level sampling statistics, recirculation, stagnant wall-layer, or repeated-exposure correction is included
## Appendices

## Next Logical Extensions

- replace the top-hat capsule geometry with nonuniform optical intensity weighting
- model local velocity distribution near the side window
- include residence-time weighting over the swept capsule
- couple penetration depth to density and wavelength
- add uncertainty bands for penetration depth, bulk density, and local velocity
- validate the capsule effective sample size proxy against tracer experiments or PAT spectral-response data
## Exported artifacts

CSV files

- results_full.csv
- summary_table.csv
- penetration_depth_table.csv
- acquisition_time_table.csv
- input_summary.csv

Figure files

- plot_01_instant_swept_unique_vs_penetration_depth.png
- plot_02_effective_sample_size_vs_penetration_depth_by_density.png
- plot_03_powder_advance_vs_acquisition_time.png
- plot_04_effective_sample_size_vs_acquisition_time_by_density.png
- plot_05_swept_increment_mass_vs_acquisition_time_by_density.png
- plot_06_heatmap_effective_sample_size_density_04.png
- plot_07_heatmap_effective_sample_size_density_05.png
- plot_08_heatmap_effective_sample_size_density_06.png
- plot_09_time_weighted_proxy_vs_acquisition_time_by_density.png
- schematic_swept_capsule_geometry.png
