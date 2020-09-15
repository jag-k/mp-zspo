from enum import Enum
from typing import Iterable, Any


class IconType(Enum):
    brands = "brands"
    regular = "regular"
    solid = "solid"


class Icon:
    def __init__(self, icon: str, icon_type: IconType = IconType.brands, **kwargs):
        self.icon = icon,
        self.icon_type = icon_type
        self.kwargs = kwargs

    def __str__(self):
        return icon(self.icon, self.icon_type.name, **self.kwargs)


class MenuTab:
    def __init__(self, name: str, groups_or_items: Iterable[Any[MenuGroup, MenuItem]] = None):
        if groups_or_items is None:
            groups_or_items = []

        self.name = name
        self.goi = list(groups_or_items)


class MenuGroup:
    def __init__(self, name: str, items: Iterable[MenuItem] = None, icon: Icon = None):
        if items is None:
            items = []

        for i in items:
            i.group(self)

        self.name = name
        self.items = items
        self.icon = icon
        self.expanded = False

