"""
InMemoryRepository - Persistance en mémoire
"""


class InMemoryRepository:
    """Repository stockant les données en mémoire"""

    def init(self):
        """Initialise les dictionnaires de stockage"""
        self._storage = {
            'User': {},
            'Place': {},
            'Review': {},
            'Amenity': {}
        }

    def add(self, obj):
        """Ajoute un objet"""
        class_name = obj.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][obj.id] = obj
        return obj

    def get(self, cls, obj_id):
        """Récupère un objet par ID"""
        class_name = cls.name
        return self._storage.get(class_name, {}).get(obj_id)

    def all(self, cls):
        """Récupère tous les objets d'un type"""
        class_name = cls.name
        return list(self._storage.get(class_name, {}).values())

    def update(self, obj):
        """Met à jour un objet"""
        obj.save()
        return obj

    def delete(self, obj):
        """Supprime un objet"""
        class_name = obj.__class__.__name__
        if class_name in self._storage and obj.id in self._storage[class_name]:
            del self._storage[class_name][obj.id]
            return True
        return False

    def find_by_email(self, email):
        """Trouve un utilisateur par email"""
        for user in self._storage.get('User', {}).values():
            if user.email == email.lower():
                return user
        return None

    def get_reviews_by_place(self, place_id):
        """Récupère tous les avis d'un lieu"""
        return [r for r in self._storage.get('Review', {}).values() 
                if r.place_id == place_id]
