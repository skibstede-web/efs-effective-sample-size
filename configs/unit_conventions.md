# Unit Conventions

## Internal SI Units
- length: `m`
- area: `m^2`
- volume: `m^3`
- time: `s`
- mass: `kg`
- density: `kg/m^3`
- velocity: `m/s`
- mass flow: `kg/s`
- particle diameter: `m`

## Typical Engineering Input Units
- `mm`, `cm`
- `g/cm^3`
- `kg/h`
- `um`
- `mg`

## Naming Convention
Use `parameter_name_unit` (example: `probe_diameter_m`, `mass_flow_rate_kg_s`).

## Standardization Rule
All user-facing input values must be standardized into internal SI units before any calculations.

## Separation Rule
Derived quantities must be stored separately from raw user inputs and standardized inputs.
