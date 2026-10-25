# E8 Artwork — String Theory

*La beleco savos la mondon* — “Beauty will save the world.”

Art-science work by Sophia Mai, exhibited at
[ISAP 2026, 13th Heidelberg Laureate Forum](https://demian-goos.de/isap-2026-13th-hlf/artworks/sophia-mai/).
The title is in Esperanto and refers to Dostoevsky's *The Idiot*.

![La beleco savos la mondon](output/Sophia_MAI_artwork.png)

The composition places the 240 roots of E8 between two physical worlds:

- **Left:** a stylized atom representing quantum mechanics.
- **Centre:** the E8 root system projected onto the Coxeter plane.
- **Right:** a distorted space-time grid, an orbiting body and a curved
  light ray representing general relativity.

A vibrating thread passes through the mandala and connects the two sides.
It evokes heterotic string theory, whose E8 × E8 formulation motivates the
choice of E8 as the central motif. The image expresses a hope for
unification; it is not a physical model or an experimentally established
account of quantum gravity.

## Toward unification

![Diagram illustrating the aspiration to unify the fundamental interactions](output/Sophia_MAI_plot.png)

This accompanying diagram illustrates the theme of unification. The Python
script generates the artwork, not this diagram.

## Mathematical construction

The script constructs the E8 root system in eight dimensions:

- 112 roots of the form ±eᵢ ± eⱼ, with i < j;
- 128 roots of the form (±½)⁸, with an even number of minus signs.

It checks that the resulting array has shape (240, 8) and that every root
has squared norm 2. A Coxeter element is constructed from eight simple
root reflections; its eigenvectors determine the projection plane. Edges
connect roots at the minimum nonzero distance in eight dimensions.

The atom, space-time grid and light ray are stylized illustrations.

## Run

Requires Python 3, NumPy and Matplotlib.

```bash
python3 -m pip install -r requirements.txt
python3 la_beleco_savos_la_mondon.py
```

Running the script writes `output/Sophia_MAI_artwork.png` and
`output/Sophia_MAI_artwork.svg`, replacing those files if they already exist.
The PNG is exported at 300 dpi.

## Files

- `la_beleco_savos_la_mondon.py` — artwork generation.
- `requirements.txt` — Python dependencies.
- `output/Sophia_MAI_artwork.png` — final raster artwork.
- `output/Sophia_MAI_artwork.svg` — vector export.
- `output/Sophia_MAI_plot.png` — accompanying diagram.
