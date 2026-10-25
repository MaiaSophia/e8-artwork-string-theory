# E8 Artwork — String Theory

## *La beleco savos la mondon*

Art-science work exhibited at **ISAP 2026, 13th Heidelberg Laureate Forum**:
👉 [demian-goos.de/isap-2026-13th-hlf/artworks/sophia-mai](https://demian-goos.de/isap-2026-13th-hlf/artworks/sophia-mai/)

![La beleco savos la mondon](output/Sophia_MAI_artwork.png)

*La beleco savos la mondon* means "Beauty will save the world" in
Esperanto: Dostoevsky's phrase, attributed to Prince Myshkin in
*The Idiot*.

The image shows E8 as the **dreamed bridge** between the two great theories
of physics, with no text other than the title:

- **On the left, quantum mechanics:** the atom, its nucleus and its orbits.
- **In the centre, E8:** the 240 roots of E8 projected onto the Coxeter
  plane.
- **On the right, general relativity:** the space-time grid curved by a
  mass, a planet in orbit and a deflected ray of light (gravitational
  lensing).

A vibrating string, like a guitar string fixed at both ends, runs through
E8 and links the two worlds.

## The change from a fragmented, divided understanding of the universe toward its dreamed unification

![The change from a fragmented, divided understanding of the universe toward its dreamed unification](output/Sophia_MAI_plot.png)

The strong, weak and electromagnetic forces come closer together as energy
increases. Gravity joins them only in the dream of a unified theory.

## The physical meaning

Quantum mechanics and general relativity each describe their own domain
with extraordinary experimental success, yet they remain incompatible at
very small scales, where gravity itself should become quantum. Reconciling
them is the greatest open problem in theoretical physics.

**Heterotic string theory** is one of the paths: particles become
vibrating strings, and one of the vibration modes is always the
**graviton**. Its mathematical consistency requires the 16 internal
dimensions to carry the symmetry **E8 × E8** (or SO(32) in the other
variant). E8, the largest exceptional simple Lie group, thus lies at the
heart of one of the most ambitious attempts at unification.

**A quest, not an established fact.** No prediction of string theory has
yet been confirmed by experiment. The title, borrowed from Dostoevsky, is
an aesthetic wish, not a scientific claim.

> *Reconciling quantum mechanics and general relativity is physics'
> greatest unsolved problem. Heterotic string theory (E8 × E8) is one
> dreamed path toward unification — mathematically beautiful, but not yet
> confirmed by experiment.*

## Project structure

```
e8-artwork-string-theory-2026/
├── la_beleco_savos_la_mondon.py   # the final artwork
├── requirements.txt               # Python dependencies (numpy, matplotlib)
└── output/                        # the artwork (PNG, SVG) and the diagram
```

## Usage

```bash
pip install -r requirements.txt
python3 la_beleco_savos_la_mondon.py
```

## Mathematical accuracy

The 240 roots are built from their exact definition: 112 roots
±eᵢ ± eⱼ and 128 roots (±½)⁸ with an even number of minus signs. At every
run, the code checks with `assert` that there are exactly 240 roots in
dimension 8, all with squared norm 2.
