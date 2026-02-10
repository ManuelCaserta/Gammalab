"""
Export helpers for Plotly figures.

Provides:
- PNG export
- PDF export
- Single-page report PDF with multiple charts
"""

from __future__ import annotations

from io import BytesIO
from typing import Optional

import plotly.graph_objects as go


def figure_to_png(fig: go.Figure, width: int = 1200, height: int = 800) -> bytes:
    """Convert a Plotly figure to PNG bytes."""
    try:
        return fig.to_image(format="png", width=width, height=height, scale=2)
    except (ValueError, ImportError) as err:
        msg = str(err).lower()
        if "kaleido" in msg or "orca" in msg or "image" in msg:
            raise ImportError(
                "PNG export requires kaleido. Install with: pip install kaleido"
            ) from err
        raise


def figure_to_pdf(fig: go.Figure, width: int = 1200, height: int = 800) -> bytes:
    """Convert a Plotly figure to PDF bytes."""
    try:
        return fig.to_image(format="pdf", width=width, height=height)
    except (ValueError, ImportError) as err:
        msg = str(err).lower()
        if "kaleido" in msg or "orca" in msg or "image" in msg:
            raise ImportError(
                "PDF export requires kaleido. Install with: pip install kaleido"
            ) from err
        raise


def create_report_pdf(
    fig_attenuation: go.Figure,
    fig_interactions: go.Figure,
    fig_monte_carlo: Optional[go.Figure] = None,
    title: str = "GammaLab Report",
) -> bytes:
    """
    Build a single-page PDF report embedding up to 3 figures.

    Layout (landscape A4):
    - top-left: attenuation
    - top-right: interactions
    - bottom full-width: monte carlo (optional)
    """
    try:
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.utils import ImageReader
        from reportlab.pdfgen import canvas
    except ImportError as err:
        raise ImportError(
            "Multi-plot PDF report requires reportlab. Install with: pip install reportlab"
        ) from err

    attenuation_png = figure_to_png(fig_attenuation, width=1200, height=800)
    interactions_png = figure_to_png(fig_interactions, width=1200, height=800)
    monte_png = (
        figure_to_png(fig_monte_carlo, width=1200, height=800)
        if fig_monte_carlo is not None
        else None
    )

    page_w, page_h = landscape(A4)
    margin = 20.0
    header_h = 28.0
    gutter = 12.0

    content_top = page_h - margin - header_h
    content_bottom = margin
    content_h = content_top - content_bottom
    content_w = page_w - (2 * margin)

    # Two-column top layout.
    top_h = content_h * (0.52 if monte_png is not None else 1.0)
    bottom_h = content_h - top_h - (gutter if monte_png is not None else 0.0)
    half_w = (content_w - gutter) / 2.0

    out = BytesIO()
    pdf = canvas.Canvas(out, pagesize=landscape(A4))
    pdf.setTitle(title)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(margin, page_h - margin - 14, title)

    def _draw_image(img_bytes: bytes, x: float, y: float, w: float, h: float) -> None:
        pdf.drawImage(ImageReader(BytesIO(img_bytes)), x, y, width=w, height=h, preserveAspectRatio=True, anchor="c")

    top_y = content_bottom + (bottom_h + gutter if monte_png is not None else 0.0)
    _draw_image(attenuation_png, margin, top_y, half_w, top_h)
    _draw_image(interactions_png, margin + half_w + gutter, top_y, half_w, top_h)

    if monte_png is not None:
        _draw_image(monte_png, margin, content_bottom, content_w, bottom_h)

    pdf.showPage()
    pdf.save()
    return out.getvalue()

