# Unsupported Claims Register

The following statements must not appear as verified outcomes unless new
evidence is added.

- “All controller-logic blocks were recovered unchanged.” Three public designs
  are portable reconstructions; the recovered mux project also references a
  decoder file outside the submitted archive.
- “Original Vivado projects were not found.” Four projects and XSim context were
  found; what is missing is implementation and board evidence.
- “The original VHDL testbenches passed.” They have no assertions. Only
  `STIMULUS_COMPLETE` is supported; the separate portable suite supports PASS.
- “The PowerWorld model validates 3.0–5.38 GW transfer.” The rerun source case
  at 2214 MW blacked out. Report stages and saved-case state are separate.
- “The transformer achieved 96.36% efficiency in hardware.” This is a
  calculation result, not a measured result.
- “The motor controller ran at one definitive switching frequency.” Recovered
  sources contain 20, 25, and approximately 30 kHz variants.
- “The microstrip was validated exactly at 3.5 GHz.” The recovered marker is at
  3.7 GHz.
- “The branch-line hybrid demonstrated −90° phase balance.” The report states
  the design objective but does not provide a numeric phase-validation result.
- “The diffusion model improved SAR quality.” No dataset, training run, metric,
  or implementation was supplied.
- Any public description of the withheld VRET source filenames, customer
  details, schemas, or development content.
