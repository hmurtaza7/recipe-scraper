from .links_backlog import LinksBacklog
from .recipe import Recipe


def all_models():
    models_obj = {
        LinksBacklog: LinksBacklog,
        Recipe: Recipe
    }
    return models_obj

__all__ = ["all_models"]

name = "models"
