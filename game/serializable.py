import json

class Serializable():
    def toJSON(self)->str:
        return json.dumps(self, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else None, 
            sort_keys=True, indent=4)