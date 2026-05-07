# Setup D: Renewal-Based ESS Versus Subscan Multiplication

## Question addressed

For Setup D, estimate the effective sample size for one 1.8 s spectrum acquired as 150 subscans at 12 ms each, then compare that estimate with a simpler shortcut:

- take a static effective sample size of about 12 mg
- multiply by 150 subscans
- conclude an effective sample size of about 1800 mg

The purpose of this note is to determine which approach is more correct within the modeling framework already used in Setup D.

## Short conclusion

Within the Setup D notebook, the renewal-based approach is the correct one of the two. The simple 12 mg x 150 shortcut is not physically consistent with the flow model in the notebook and overestimates the effective sample size by roughly one to two orders of magnitude over the modeled operating range.

The key reason is that subscan count is not the same as the number of independent powder renewals at the probe. In Setup D, the appropriate multiplier on the static optical mass is the renewal count

$$
N_{\mathrm{refresh}} = \frac{v\,t_{\mathrm{acq}}}{d_{\mathrm{probe}}}
$$

not the instrument subscan count.

## Setup D model used in the notebook

The Setup D notebook models one spectrum as a renewal problem at a fixed probe in a flowing powder pipe.

Instantaneous optical mass:

$$
m_{\mathrm{opt}} = \rho\,A_{\mathrm{probe}}\,d_{\mathrm{pen}}
$$

Superficial velocity:

$$
v = \frac{\dot{m}}{\rho\,A_{\mathrm{pipe}}}
$$

Renewal factor during one acquisition:

$$
N_{\mathrm{refresh}} = \frac{v\,t_{\mathrm{acq}}}{d_{\mathrm{probe}}}
$$

Effective sample size proxy:

$$
m_{\mathrm{eff,proxy}} = m_{\mathrm{opt}}\,N_{\mathrm{refresh}}
= \rho\,A_{\mathrm{probe}}\,d_{\mathrm{pen}}\left(\frac{v\,t_{\mathrm{acq}}}{d_{\mathrm{probe}}}\right)
$$

This can also be written as:

$$
m_{\mathrm{eff,proxy}} = \left(\frac{A_{\mathrm{probe}}\,d_{\mathrm{pen}}\,t_{\mathrm{acq}}}{d_{\mathrm{probe}}\,A_{\mathrm{pipe}}}\right)\dot{m}
$$

For the fixed Setup D geometry and 1.8 s acquisition time used in the notebook, this reduces to:

$$
m_{\mathrm{eff,proxy}}\,[\mathrm{mg}] = 0.591716\;\dot{m}_{\mathrm{kg/h}}\;d_{\mathrm{pen,mm}}
$$

So for a 1.0 mm penetration depth:

- at 40 kg/h: 23.67 mg
- at 95 kg/h: 56.21 mg
- at 100 kg/h: 59.17 mg

For a 2.0 mm penetration depth, those values double.

## Relation to the static sample size

The static Setup A model gives:

$$
m_{\mathrm{static}} = \rho\,A_{\mathrm{probe}}\,d_{\mathrm{pen}}
$$

For the same 5 mm probe, this becomes:

$$
m_{\mathrm{static}}\,[\mathrm{mg}] = 19.634954\;\rho_{\mathrm{g/cm^3}}\;d_{\mathrm{pen,mm}}
$$

A static optical mass of about 12 mg corresponds closely to the case:

- density about 0.6 g/cm^3
- penetration depth about 1.0 mm

which gives:

$$
m_{\mathrm{static}} \approx 11.781\;\mathrm{mg}
$$

The Setup D model can therefore be written as:

$$
m_{\mathrm{eff,proxy}} = m_{\mathrm{static}}\,N_{\mathrm{refresh}}
$$

This means the dynamic problem does indeed start from the same static optical mass concept, but the correct multiplier is the number of probe-scale renewals during the full 1.8 s spectrum, not the number of 12 ms detector integrations.

## Why multiplying by 150 subscans is not correct

The shortcut

$$
12\;\mathrm{mg} \times 150 = 1800\;\mathrm{mg}
$$

implicitly assumes that every 12 ms subscan measures a completely fresh, non-overlapping probe footprint. In Setup D terms, that would require:

$$
v\,t_{\mathrm{subscan}} \approx d_{\mathrm{probe}}
$$

With:

- subscan time = 0.012 s
- probe diameter = 5 mm = 0.5 cm

the required velocity would be:

$$
v_{\mathrm{required}} = \frac{0.5}{0.012} = 41.67\;\mathrm{cm/s}
$$

That corresponds to a required throughput of about:

- 1991 kg/h at 0.4 g/cm^3
- 2489 kg/h at 0.5 g/cm^3
- 2986 kg/h at 0.6 g/cm^3

Those values are far above the modeled Setup D range of 40 to 100 kg/h.

Within the actual Setup D operating window, the notebook predicts only partial movement of the powder during one 12 ms subscan:

- at 40 kg/h and 0.4 g/cm^3: about 0.10 mm per subscan
- at 95 kg/h and 0.4 g/cm^3: about 0.24 mm per subscan
- at 95 kg/h and 0.6 g/cm^3: about 0.16 mm per subscan
- at 100 kg/h and 0.6 g/cm^3: about 0.17 mm per subscan

Compared with a 5 mm probe diameter, each subscan advances only about 1 to 5 percent of one probe diameter. So successive subscans are heavily overlapping in space and cannot be treated as 150 independent static samples.

## What the correct multiplier looks like instead

The relevant multiplier is the renewal count over the full 1.8 s acquisition.

Representative cases for 1.0 mm penetration depth are:

| Throughput | Density | Renewal count | ESS proxy |
|---|---:|---:|---:|
| 40 kg/h | 0.4 g/cm^3 | 3.01 | 23.67 mg |
| 95 kg/h | 0.4 g/cm^3 | 7.16 | 56.21 mg |
| 95 kg/h | 0.6 g/cm^3 | 4.77 | 56.21 mg |
| 100 kg/h | 0.6 g/cm^3 | 5.02 | 59.17 mg |

Two points matter here:

1. The number of effective renewals is of order 3 to 8, not 150.
2. At fixed throughput and this specific model, density cancels in the final proxy because higher density increases instantaneous optical mass but decreases superficial velocity by the same factor.

The density cancellation does not mean density never matters physically. It means it cancels within this particular first-order model.

## A stronger physical consistency check

The Setup D notebook also reports a convective reference mass passed by the probe footprint during one acquisition:

$$
m_{\mathrm{passed}} = \rho\,v\,A_{\mathrm{probe}}\,t_{\mathrm{acq}}
$$

For the 1.8 s Setup D cases, this reference mass is about:

- 118.34 mg at 40 kg/h
- 281.07 mg at 95 kg/h
- 295.86 mg at 100 kg/h

The 1800 mg shortcut is not just larger than the notebook ESS proxy. It is even much larger than the total convective reference mass presented past the probe footprint under the same transport model. That makes 1800 mg internally inconsistent with the Setup D framework.

## Comparison of the two approaches

### Approach 1: Renewal-based Setup D proxy

Strengths:

- consistent with the actual Setup D geometry
- uses powder flow to determine how much new material is presented during one spectrum
- respects the difference between axial renewal and radial optical penetration
- consistent with the notebook algebra and exported tables

Limitations:

- still a proxy, not a full statistical ESS
- uses superficial velocity rather than a resolved lower-wall velocity
- does not resolve revisit, residence-time distribution, or detailed radiative transfer

### Approach 2: Static mass x 150 subscans

Strengths:

- simple and intuitive
- may be useful as a rough upper-bound thought experiment if every subscan were independent

Weaknesses:

- assumes full probe-scale renewal every 12 ms
- ignores strong overlap between consecutive subscans
- ignores the actual powder velocity and probe crossing time
- produces values larger than the mass-presentation scale of the Setup D model

## Judgement

Of the two approaches, the renewal-based Setup D calculation is the more correct one by a wide margin.

The shortcut of multiplying a static mass by the number of subscans confuses:

- detector averaging steps
- with independent powder renewals at the probe

Those are not the same thing. In Setup D, one full spectrum consists of 150 electronic integrations, but only a few probe-scale physical renewals of powder. The notebook model is built exactly around that distinction.

## Practical recommendation

For Setup D, estimate one-spectrum effective sample size as:

$$
m_{\mathrm{eff,proxy}} = m_{\mathrm{static}}\left(\frac{v\,t_{\mathrm{acq}}}{d_{\mathrm{probe}}}\right)
$$

not as:

$$
m_{\mathrm{static}} \times N_{\mathrm{subscans}}
$$

If a more rigorous absolute ESS is needed, the next model step is not subscan multiplication. It is to extend Setup D with:

- local wall velocity rather than superficial velocity
- repeated-presentation or revisit statistics
- time-weighted spectral contribution
- optical weighting beyond a uniform cylindrical depth

Until then, the renewal-based proxy is the correct interpretation of Setup D, while 12 mg x 150 should be treated as an unrealistic upper-bound style heuristic rather than a valid ESS estimate.