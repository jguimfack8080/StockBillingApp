import os

def create_project_structure():
    structure = {
        "auth_service": ["Dockerfile", "requirements.txt", "main.py", "models.py", "schemas.py", "routers/auth.py", "routers/users.py"],
        "sales_service": ["Dockerfile", "requirements.txt", "main.py", "models.py", "schemas.py", "routers/sales.py"],
        "stock_service": ["Dockerfile", "requirements.txt", "main.py", "models.py", "schemas.py", "routers/stock.py"],
    }
    
    for service, files in structure.items():
        os.makedirs(service, exist_ok=True)
        os.makedirs(os.path.join(service, "routers"), exist_ok=True)
        
        for file in files:
            file_path = os.path.join(service, file)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                f.write("")  # Création de fichiers vides
    
    # Création de docker-compose.yml et init.sql
    open("docker-compose.yml", "w").close()
    open("init.sql", "w").close()
    
    print("Structure du projet créée avec succès !")

if __name__ == "__main__":
    create_project_structure()
