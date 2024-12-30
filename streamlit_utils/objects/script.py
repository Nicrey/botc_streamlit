
class Script: 

    def __init__(self, json_dict, file_path):
        self.json_dict = json_dict
        self.path = file_path
        self.town = []
        self.outsider = []
        self.minion = []
        self.demon = []
        self.author = "Unknown"
        self.name = "Unknown"
        for entry in json_dict:
            if "author" in entry:
                self.author = entry["author"]
                self.name = entry.get("name", "Unknown")
                continue
            
            if entry["team"] == "townsfolk":
                self.town.append(entry["name"])
            if entry["team"] == "outsider":
                self.outsider.append(entry["name"])
            if entry["team"] == "minion":
                self.minion.append(entry["name"])                            
            if entry["team"] == "demon":
                self.demon.append(entry["name"])                
        

    def contains_role(self,r):
        return r in self.town + self.outsider + self.minion + self.demon
    
    def __str__(self):
        return self.name + " | " + self.author


