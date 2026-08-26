from dataclasses import dataclass


@dataclass
class FeaturedFigure:
    id: int | None
    figure_id: int
    priority: int
