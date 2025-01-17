from arcgis.gis import GIS



def authenticate(url: str, username: str, password: str) -> GIS:
    """
    Authenticates against ArcGIS Online using username and password.

    :param url: Optional string. If URL is None, then the URL will be ArcGIS Online.
    :param username: The name of the user.
    :param password: The password of the user.
    """
    # Login to your arcgis account
    return GIS(url, username, password)