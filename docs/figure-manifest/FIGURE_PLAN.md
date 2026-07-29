# Figure Plan

The visual hierarchy follows a reusable engineering-story pattern: identity,
system flow, module detail, and evidence near the claim. It does not copy any
third-party branding or artwork.

| Course | Identity figure | System flow | Evidence board | Boundary figure |
|---|---|---|---|---|
| Controller Logic | RTL progression | source → compile → stimulus → assertion → VCD | original XSim archive + local GHDL traces | recovered vs reconstructed |
| Transformer | winding architecture | requirements → Kg → core → losses → decision | UI/EI/DU comparison | calculation vs hardware |
| Power Systems | 765 kV π model | inputs → Zc/SIL → case model → diagnostic | report stages + PowerWorld 24 rerun | source report vs tool rerun |
| Motor Control | cascaded PI architecture | reference → speed PI → current PI → plant | frequency/source consistency table | archive vs rerun |
| RF/Microwave | passive-network map | independent Homework 2/4/5 paths | selected Cadence frames beside values | marker/design-frequency limits |
| Sensor | AESA-SAR architecture | acquisition → formation → proposed diffusion → ATR | literature-derived architecture only | no dataset/model/result |

Every public figure must have a manifest row, source class, caption, alt text,
and explicit claim boundary.
