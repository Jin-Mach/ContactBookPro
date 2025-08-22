from typing import Any
from folium import Map, Marker, Element, plugins
from folium.plugins import MarkerCluster

from src.utilities.application_support_provider import ApplicationSupportProvider
from src.utilities.logger_provider import get_logger


# noinspection PyUnresolvedReferences
def create_map(contacts: list[dict[str, Any]]) -> str | None:
    try:
        latitude = 0.0
        longitude = 0.0
        start_zoom = 2
        location_data = ApplicationSupportProvider.get_default_location()
        if location_data:
            location = location_data.get("location", {})
            latitude = location.get("latitude", 0.0)
            longitude = location.get("longitude", 0.0)
            if latitude != 0.0 and longitude != 0.0:
                start_zoom = 8
        folium_map = Map(location=(latitude, longitude), zoom_start=start_zoom, min_zoom=2)
        disable_context_menu = Element("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var mapElement = document.querySelector('.folium-map');
                if (mapElement) {
                    mapElement.addEventListener('contextmenu', function(event) {
                        event.preventDefault();
                    });
                }
            });
        </script>
        """)
        remove_titles = Element("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Počkej chvilku, než se Mapa vykreslí
                setTimeout(function() {
                    document.querySelectorAll('.leaflet-control-zoom a').forEach(function(el) {
                        el.removeAttribute('title');
                    });
                }, 500);
            });
        </script>
        """)
        folium_map.get_root().html.add_child(disable_context_menu)
        folium_map.get_root().html.add_child(remove_titles)
        marker_cluster = MarkerCluster()
        marker_cluster.add_to(folium_map)
        for contact in contacts:
            popup_str = (f"{contact.get('first_name', '')} {contact.get('second_name', '')}\n"
                        f"{contact.get('email', '')}\n"
                        f"{contact.get('phone_number', '')}")
            marker = Marker(location=[contact.get("latitude"), contact.get("longitude")], popup=popup_str)
            marker.add_to(marker_cluster)
        minimap = plugins.MiniMap()
        folium_map.add_child(minimap)
        html = folium_map.get_root().render()
        return html
    except Exception as e:
        logger = get_logger()
        logger.error(f"{create_map.__name__} : {e}", exc_info=True)
        return None