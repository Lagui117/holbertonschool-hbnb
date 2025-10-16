"""
InMemoryRepository - Persistance en mémoire
"""


class InMemoryRepository:
    def __init__(self):
        """Initialize the in-memory storage"""
        self._storage = {}

    def add(self, entity):
        """Add an entity to the repository"""
        class_name = entity.__class__.__name__
        if class_name not in self._storage:
            self._storage[class_name] = {}
        self._storage[class_name][entity.id] = entity
        return entity

    def get(self, cls, entity_id):
        """Get an entity by class and ID"""
        class_name = cls.__name__
        return self._storage.get(class_name, {}).get(entity_id)

    def all(self, cls):
        """Get all entities of a class"""
        class_name = cls.__name__
        return list(self._storage.get(class_name, {}).values())

    def update(self, obj):
        """Update an existing object"""
        class_name = obj.__class__.__name__
        obj_id = obj.id
        
        # Vérifie que l'objet existe avant de le mettre à jour
        if class_name not in self._storage or obj_id not in self._storage[class_name]:
            raise ValueError(f"{class_name} with id {obj_id} not found")
        
        # Met à jour le timestamp si la méthode save() existe
        if hasattr(obj, 'save'):
            obj.save()
        
        # Stocke l'objet mis à jour
        self._storage[class_name][obj_id] = obj
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