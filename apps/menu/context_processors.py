from .models import Menu


def access_menu_items(request) -> dict:
    """
      The context processor return a dictionary with menu item.
    """
    menu_items = Menu.objects.filter(show_item=True)
    return {'menu_items': menu_items}
