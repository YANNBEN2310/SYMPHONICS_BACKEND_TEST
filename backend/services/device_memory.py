from typing import Dict, Any


class DeviceStateMemory:
    """
    cacher en mémoire de le state des device.
    Permet de capter que les valeurs ayant changé.
    """

    def __init__(self):
        # structure :
        # { dev_id: { code: last_value } }
        self._cache: Dict[str, Dict[str, Any]] = {}

    def has_changed(self, dev_id: str, code: str, new_value: Any) -> bool:
        """
        retourne True si la valeur a changé depuis la dernière fois.
        Met à jour le cache si nécessaire.
        
        """
        if dev_id not in self._cache:
            self._cache[dev_id] = {code: new_value}
            return True

        device_values = self._cache[dev_id]

        if code not in device_values:
            device_values[code] = new_value
            return True

        if device_values[code] != new_value:
            device_values[code] = new_value
            return True

        return False
