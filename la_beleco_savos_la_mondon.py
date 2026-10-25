#!/usr/bin/env python3

"""Render "La beleco savos la mondon": an E8 mandala linking quantum and relativity motifs."""

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import LineCollection
from matplotlib.colors import to_rgb
from itertools import combinations, product


# Output files and rendering settings.
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
PNG_PATH = os.path.join(OUTPUT_DIR, "Sophia_MAI_artwork.png")
SVG_PATH = os.path.join(OUTPUT_DIR, "Sophia_MAI_artwork.svg")

DPI = 300
WIDTH_INCHES = 18.71
HEIGHT_INCHES = 13.23


BACKGROUND_COLOR = "#050510"

MANDALA_COLORMAP = "hsv"
ACCENT_COLOR = "#FFC400"
EDGE_COLOR = "#D6D6FF"

NUCLEUS_COLOR = ACCENT_COLOR
ORBIT_COLOR = "#8A3FFC"
ELECTRON_COLOR = "#FF1464"

MASS_COLOR = ACCENT_COLOR
GRID_COLOR = "#1E6FFF"
PLANET_COLOR = "#00E676"
LIGHT_COLOR = "#FFEE00"


STRING_INNER_COLOR = tuple(0.55 * np.array(to_rgb(ACCENT_COLOR))
                            + 0.45 * np.array(to_rgb(EDGE_COLOR)))
STRING_OUTER_COLOR = EDGE_COLOR


def generate_e8_roots():
    """Return the 112 integer roots and 128 half-integer roots of E8."""
    roots = []
    for i, j in combinations(range(8), 2):
        for si, sj in product([1.0, -1.0], repeat=2):
            v = np.zeros(8)
            v[i], v[j] = si, sj
            roots.append(v)
    for signs in product([1.0, -1.0], repeat=8):
        if signs.count(-1.0) % 2 == 0:
            roots.append(0.5 * np.array(signs))
    return np.array(roots)


def validate_roots(roots):
    """Check the root count, dimension and squared norms."""
    assert roots.shape == (240, 8), f"Expected 240 roots in 8 dimensions, got {roots.shape}"
    squared_norms = np.sum(roots ** 2, axis=1)
    assert np.allclose(squared_norms, 2.0, atol=1e-9), "All roots must have squared norm 2"


def e8_simple_roots():
    """Return eight simple roots in the Bourbaki convention."""
    e = np.eye(8)
    a1 = 0.5 * (e[0] - e[1] - e[2] - e[3] - e[4] - e[5] - e[6] + e[7])
    a2 = e[0] + e[1]
    a3 = e[1] - e[0]
    a4 = e[2] - e[1]
    a5 = e[3] - e[2]
    a6 = e[4] - e[3]
    a7 = e[5] - e[4]
    a8 = e[6] - e[5]
    return np.array([a1, a2, a3, a4, a5, a6, a7, a8])


def coxeter_element(simple_roots):
    """Compose the reflections associated with the simple roots."""
    c = np.eye(8)
    for alpha in simple_roots:
        c = (np.eye(8) - np.outer(alpha, alpha)) @ c
    return c


def coxeter_plane_basis(c, h=30):
    """Return an orthonormal basis for the Coxeter plane (h = 30)."""
    eigenvalues, eigenvectors = np.linalg.eig(c)
    target = np.exp(2j * np.pi / h)
    idx = np.argmin(np.abs(eigenvalues - target))
    eigenvector = eigenvectors[:, idx]
    u = np.real(eigenvector)
    v = np.imag(eigenvector)
    u = u / np.linalg.norm(u)
    v = v - np.dot(v, u) * u
    v = v / np.linalg.norm(v)
    return u, v


def project_onto_plane(roots, u, v):
    """Project the roots onto the plane spanned by u and v."""
    return roots @ u, roots @ v


def nearest_neighbor_edges(roots):
    """Return each pair of roots at the minimum nonzero distance."""
    gram = roots @ roots.T
    squared_norms = np.sum(roots ** 2, axis=1)
    dist2 = np.clip(squared_norms[:, None] + squared_norms[None, :] - 2 * gram, 0, None)
    distances = np.sqrt(dist2)
    min_distance = distances[distances > 1e-9].min()
    mask = np.isclose(distances, min_distance, atol=1e-6)
    i_idx, j_idx = np.where(np.triu(mask, k=1))
    return i_idx, j_idx


def draw_glow(ax, x, y, radius, color, zorder=5, n_layers=5, alpha_max=0.16):
    """Draw a bright point over concentric translucent disks."""
    for k in range(n_layers, 0, -1):
        r = radius * k / n_layers
        a = alpha_max * (1 - k / (n_layers + 1))
        ax.add_patch(Circle((x, y), r, color=color, alpha=a, linewidth=0, zorder=zorder))
    ax.add_patch(Circle((x, y), radius * 0.30, color=color, alpha=0.95, linewidth=0, zorder=zorder + 1))


def draw_tendril(ax, ring_radius, angle_deg, reach=0.42, color=EDGE_COLOR,
                       n_points=80, zorder=2.5):
    """Extend a fading curve beyond the outer ring of the mandala."""
    a0 = np.radians(angle_deg)
    t = np.linspace(0, 1, n_points)
    radial_positions = ring_radius * (1 + reach * t)
    angular_offset = np.radians(5) * np.sin(2 * np.pi * t)
    angles = a0 + angular_offset
    x = radial_positions * np.cos(angles)
    y = radial_positions * np.sin(angles)

    points = np.stack([x, y], axis=1).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    alphas = 0.30 * (1 - t[:-1])
    colors = np.tile(np.array([*to_rgb(color)]), (len(segments), 1))
    colors = np.concatenate([colors, alphas[:, None]], axis=1)

    lines = LineCollection(segments, colors=colors, linewidths=1.0, zorder=zorder, capstyle="round")
    lines.set_clip_on(False)
    ax.add_collection(lines)


def draw_e8_panel(ax, x, y, i_idx, j_idx):
    """Draw the projected roots, edges and string crossing."""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.set_aspect("equal")
    ax.axis("off")

    radii = np.hypot(x, y)
    min_radius, max_radius = radii.min(), radii.max()
    margin = max_radius * 1.14
    ax.set_xlim(-margin, margin)
    ax.set_ylim(-margin, margin)

    color_values = (np.arctan2(y, x) + np.pi) / (2 * np.pi)
    cmap = plt.get_cmap(MANDALA_COLORMAP)

    segments = np.stack([
        np.stack([x[i_idx], y[i_idx]], axis=1),
        np.stack([x[j_idx], y[j_idx]], axis=1),
    ], axis=1)
    edge_colors = cmap((color_values[i_idx] + color_values[j_idx]) / 2)
    ax.add_collection(LineCollection(segments, colors=edge_colors,
                                      linewidths=0.22, alpha=0.32, zorder=2))

    for size_multiplier, alpha in [(7, 0.05), (3.5, 0.12)]:
        ax.scatter(x, y, c=color_values, cmap=MANDALA_COLORMAP, s=17 * size_multiplier,
                   alpha=alpha, zorder=3, linewidths=0)
    ax.scatter(x, y, c=color_values, cmap=MANDALA_COLORMAP, s=17,
               zorder=4, edgecolors="white", linewidths=0.2)

    for angle_deg in (160, 180, 200):
        draw_tendril(ax, max_radius, angle_deg)
    for angle_deg in (-20, 0, 20):
        draw_tendril(ax, max_radius, angle_deg)

    # The crossing leaves a gap at the origin.
    left_crossing_points, right_crossing_points = draw_mandala_crossing(ax, margin, STRING_INNER_COLOR)

    return min_radius, max_radius, left_crossing_points, right_crossing_points


def draw_atom(ax, scale=1.0):
    """Draw a stylized atom with three elliptical orbits."""
    theta = np.linspace(0, 2 * np.pi, 300)
    a, b = 0.95 * scale, 0.40 * scale

    electron_positions = []
    for k, angle_deg in enumerate((0, 60, 120)):
        phi = np.radians(angle_deg)
        ex = a * np.cos(theta)
        ey = b * np.sin(theta)

        x_rot = ex * np.cos(phi) - ey * np.sin(phi)
        y_rot = ex * np.sin(phi) + ey * np.cos(phi)
        ax.plot(x_rot, y_rot, color=ORBIT_COLOR, linewidth=2.0, alpha=0.8, zorder=3)


        t_e = 0.35 + 0.5 * k
        ex_pt, ey_pt = a * np.cos(t_e), b * np.sin(t_e)
        electron_positions.append((
            ex_pt * np.cos(phi) - ey_pt * np.sin(phi),
            ex_pt * np.sin(phi) + ey_pt * np.cos(phi),
        ))

    for ex, ey in electron_positions:
        draw_glow(ax, ex, ey, radius=0.075 * scale, color=ELECTRON_COLOR, zorder=6, alpha_max=0.32)

    draw_glow(ax, 0, 0, radius=0.20 * scale, color=NUCLEUS_COLOR, zorder=6, alpha_max=0.24)


def draw_quantum_panel(ax):
    """Draw the left panel."""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)

    draw_atom(ax, scale=1.15)


def radial_displacement(x, y, cx=0.0, cy=0.0, amplitude=3.5, scale=0.38):
    """Compress radii around (cx, cy) without folding the grid."""
    dx, dy = x - cx, y - cy
    r = np.hypot(dx, dy)
    safe_radius = np.where(r < 1e-9, 1e-9, r)
    factor = 1.0 / (1.0 + amplitude / ((safe_radius / scale) ** 2 + 1.0))
    new_radius = safe_radius * factor
    return cx + dx / safe_radius * new_radius, cy + dy / safe_radius * new_radius


def draw_spacetime_grid(ax, half_extent=1.55, n_lines=15, n_samples=220):
    """Draw a grid distorted by radial_displacement."""
    grid_positions = np.linspace(-half_extent, half_extent, n_lines)
    samples = np.linspace(-half_extent, half_extent, n_samples)

    for u0 in grid_positions:
        x, y = radial_displacement(np.full_like(samples, u0), samples)
        ax.plot(x, y, color=GRID_COLOR, linewidth=0.95, alpha=0.68, zorder=2)
    for v0 in grid_positions:
        x, y = radial_displacement(samples, np.full_like(samples, v0))
        ax.plot(x, y, color=GRID_COLOR, linewidth=0.95, alpha=0.68, zorder=2)


def draw_orbit(ax, a=1.15, b=0.76, color=PLANET_COLOR, zorder=5):
    """Draw a fading orbital trail and a bright endpoint."""
    phi = np.linspace(np.radians(15), np.radians(345), 260)
    u, v = a * np.cos(phi), b * np.sin(phi)
    x, y = radial_displacement(u, v)

    points = np.stack([x, y], axis=1).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    alphas = np.linspace(0.05, 0.85, len(segments))
    colors = np.tile(np.array([*to_rgb(color)]), (len(segments), 1))
    colors = np.concatenate([colors, alphas[:, None]], axis=1)
    ax.add_collection(LineCollection(segments, colors=colors, linewidths=2.0, zorder=zorder))

    draw_glow(ax, x[-1], y[-1], radius=0.085, color=color, zorder=zorder + 1, alpha_max=0.3)


def light_deflection(x, center=0.0, width=0.55, amplitude=0.5):
    """Return a stylized vertical offset for the light ray."""
    return -amplitude / (1.0 + ((x - center) / width) ** 2)


def draw_light_ray(ax, y0=0.88, color=LIGHT_COLOR, zorder=7):
    """Draw a curved light ray with a directional arrow."""
    x = np.linspace(-1.6, 1.6, 300)
    y = y0 + light_deflection(x)

    for lw, a in [(5.5, 0.10), (3.2, 0.20)]:
        ax.plot(x, y, color=color, linewidth=lw, alpha=a, zorder=zorder - 1, solid_capstyle="round")
    ax.plot(x, y, color=color, linewidth=1.7, alpha=0.92, zorder=zorder, solid_capstyle="round")
    ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-8], y[-8]),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.7, alpha=0.92), zorder=zorder)


def draw_relativity_panel(ax):
    """Draw the right panel and return the central mass y-coordinate."""
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-1.65, 1.65)
    ax.set_ylim(-1.65, 1.65)

    draw_spacetime_grid(ax)
    draw_orbit(ax)
    draw_light_ray(ax)

    draw_glow(ax, 0, 0, radius=0.20, color=MASS_COLOR, zorder=6, alpha_max=0.28)

    return 0.0


def axes_edge_point(ax, side, fraction_y=0.5):
    """Return a side midpoint in figure coordinates."""
    pos = ax.get_position()
    y = pos.y0 + fraction_y * (pos.y1 - pos.y0)
    x = pos.x0 if side == "left" else pos.x1
    return np.array([x, y])


def data_to_figure_point(fig, ax, data_x, data_y):
    """Convert a point from axes data coordinates to figure coordinates."""
    return fig.transFigure.inverted().transform(ax.transData.transform((data_x, data_y)))


def _rgba_gradient(inner_color, outer_color, t, alpha):
    """Interpolate RGB colors and apply a constant alpha."""
    c1 = np.array(to_rgb(inner_color))
    c2 = np.array(to_rgb(outer_color))
    colors = c1[None, :] + (c2[None, :] - c1[None, :]) * t[:, None]
    alphas = np.full(len(t), alpha)
    return np.concatenate([colors, alphas[:, None]], axis=1)


def draw_half_string(ax_overlay, inner_point, outer_point, inner_color, outer_color,
                       n_oscillations=4.5, damping=2.6, amplitude=0.017, n_points=300, zorder=3):
    """Draw a damped sinusoid from the mandala to a side panel."""
    t = np.linspace(0, 1, n_points)
    base = inner_point[None, :] + t[:, None] * (outer_point - inner_point)[None, :]

    direction = outer_point - inner_point
    length = np.linalg.norm(direction)
    perp = np.array([-direction[1], direction[0]]) / length

    envelope = np.exp(-damping * t)
    displacement = amplitude * np.sin(n_oscillations * 2 * np.pi * t) * envelope

    pts = base + displacement[:, None] * perp[None, :]

    points = pts.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    t_mid = (t[:-1] + t[1:]) / 2

    for lw, a in [(2.6, 0.04), (1.5, 0.08)]:
        colors = _rgba_gradient(inner_color, outer_color, t_mid, a)
        ax_overlay.add_collection(LineCollection(segments, colors=colors, linewidths=lw,
                                                  zorder=zorder - 1, capstyle="round"))
    colors = _rgba_gradient(inner_color, outer_color, t_mid, 0.8)
    ax_overlay.add_collection(LineCollection(segments, colors=colors, linewidths=0.65,
                                              zorder=zorder, capstyle="round"))

    return pts


def draw_pulses(ax_overlay, pts, color, n=9, zorder=6):
    """Draw pulses that shrink and spread out toward the panel."""
    n_total = len(pts)
    fractions = np.linspace(0, 1, n) ** 2.4
    for frac in fractions:
        idx = int(frac * (n_total - 1))
        px, py = pts[idx]
        radius = 0.003 + 0.007 * (1 - frac)
        alpha = 0.12 + 0.50 * (1 - frac)
        for k in (3, 2, 1):
            ax_overlay.add_patch(Circle((px, py), radius * k / 3, color=color,
                                        alpha=alpha * (1 - k / 4), linewidth=0, zorder=zorder))
        ax_overlay.add_patch(Circle((px, py), radius * 0.35, color=color,
                                    alpha=min(alpha + 0.3, 0.95), linewidth=0, zorder=zorder + 1))


def draw_mandala_crossing(ax, margin, color, amplitude=0.045, n_oscillations=2,
                               n_points=150, gap=0.09, zorder_back=1.5, zorder_front=6.5):
    """Draw the string behind the left half and in front of the right half."""
    t = np.linspace(0, 1, n_points)
    wave = amplitude * np.sin(n_oscillations * 2 * np.pi * t) * t

    x_left = -gap - t * (margin - gap)
    left_points = np.stack([x_left, wave], axis=1)

    x_right = gap + t * (margin - gap)
    right_points = np.stack([x_right, wave], axis=1)

    color_rgb = to_rgb(color)
    for pts, zorder in [(left_points, zorder_back), (right_points, zorder_front)]:
        points = pts.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        for lw, a in [(2.2, 0.05), (1.3, 0.09)]:
            colors = np.tile([*color_rgb, a], (len(segments), 1))
            ax.add_collection(LineCollection(segments, colors=colors, linewidths=lw,
                                             zorder=zorder - 0.5, capstyle="round"))
        colors = np.tile([*color_rgb, 0.75], (len(segments), 1))
        ax.add_collection(LineCollection(segments, colors=colors, linewidths=0.55,
                                         zorder=zorder, capstyle="round"))

    return left_points, right_points


def build_figure():
    """Build the three panels and their connecting string."""
    roots = generate_e8_roots()
    validate_roots(roots)

    c = coxeter_element(e8_simple_roots())
    u, v = coxeter_plane_basis(c)
    x, y = project_onto_plane(roots, u, v)
    i_idx, j_idx = nearest_neighbor_edges(roots)

    fig = plt.figure(figsize=(WIDTH_INCHES, HEIGHT_INCHES), facecolor=BACKGROUND_COLOR)
    gs = fig.add_gridspec(
        nrows=1, ncols=3, width_ratios=[1.12, 1.0, 1.12],
        wspace=0.06,
        left=0.03, right=0.97, top=0.965, bottom=0.035,
    )

    ax_left = fig.add_subplot(gs[0, 0])
    ax_center = fig.add_subplot(gs[0, 1])
    ax_right = fig.add_subplot(gs[0, 2])

    draw_quantum_panel(ax_left)
    _, _, left_crossing_points, right_crossing_points = draw_e8_panel(ax_center, x, y, i_idx, j_idx)
    mass_y = draw_relativity_panel(ax_right)

    # Match each pulse layer to its half of the crossing.
    draw_pulses(ax_center, left_crossing_points, color=ACCENT_COLOR, n=4, zorder=1.8)
    draw_pulses(ax_center, right_crossing_points, color=ACCENT_COLOR, n=4, zorder=6.8)

    # Use figure coordinates to connect points across the three axes.
    ax_overlay = fig.add_axes([0, 0, 1, 1])
    ax_overlay.set_xlim(0, 1)
    ax_overlay.set_ylim(0, 1)
    ax_overlay.axis("off")
    ax_overlay.patch.set_alpha(0.0)

    left_center_point = axes_edge_point(ax_center, "left")
    nucleus_point = data_to_figure_point(fig, ax_left, 0, 0)
    left_points = draw_half_string(ax_overlay, left_center_point, nucleus_point,
                                   STRING_INNER_COLOR, STRING_OUTER_COLOR)
    draw_pulses(ax_overlay, left_points, color=ACCENT_COLOR)

    right_center_point = axes_edge_point(ax_center, "right")
    mass_point = data_to_figure_point(fig, ax_right, 0, mass_y)
    right_points = draw_half_string(ax_overlay, right_center_point, mass_point,
                                   STRING_INNER_COLOR, STRING_OUTER_COLOR)
    draw_pulses(ax_overlay, right_points, color=ACCENT_COLOR)

    return fig


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig = build_figure()

    fig.savefig(PNG_PATH, dpi=DPI, facecolor=fig.get_facecolor())
    fig.savefig(SVG_PATH, facecolor=fig.get_facecolor())
    plt.close(fig)

    print(f"Artwork saved to:\n  - {PNG_PATH}\n  - {SVG_PATH}")


if __name__ == "__main__":
    main()
