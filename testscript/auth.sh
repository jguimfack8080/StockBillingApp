## 1. Vérification du Serveur

Pour vérifier si le serveur est en ligne, utilisez la commande suivante :

```bash
curl -s "http://localhost:8001" | grep -q "OK" && echo "Le serveur est en ligne." || echo "Le serveur ne répond pas."
2. Obtenir un Token d'Admin
Pour obtenir un token d'admin, envoyez une requête POST avec les informations d'identification de l'admin :

bash
Kopieren
Bearbeiten
curl -X POST "http://localhost:8001/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@test.com&password=adminpassword"
Cette commande renverra un token d'authentification à utiliser pour les requêtes protégées.

3. Créer un Utilisateur
Pour créer un nouvel utilisateur, envoyez une requête POST avec les informations de l'utilisateur et un token d'admin valide :

curl -X POST "http://localhost:8001/users/" \
    -H "Authorization: Bearer your_admin_token_here" \
    -H "Content-Type: application/json" \
    -d '{
        "first_name": "Jean",
        "last_name": "Dupont",
        "birth_date": "1995-05-20",
        "id_card_number": "12345678902",
        "email": "user2@test.com",
        "password": "userpass",
        "role": "cashier"
    }'

4. Mettre à Jour un Utilisateur
Pour mettre à jour un utilisateur existant, envoyez une requête PUT avec l'ID de l'utilisateur et les informations à mettre à jour :


curl -X PUT "http://localhost:8001/users/1" \
    -H "Authorization: Bearer your_admin_token_here" \
    -H "Content-Type: application/json" \
    -d '{
        "email": "user1_updated@test.com",
        "role": "cashier"
    }'
Remarque : On par l'ID de l'utilisateur que tu souhaites mettre à jour et your_admin_token_here par le token d'admin.

5. Récupérer Tous les Utilisateurs
L'admin peut récupérer tous les utilisateurs en envoyant une requête GET. Cela nécessite un token d'admin valide :

curl -X GET "http://localhost:8001/users/" \
    -H "Authorization: Bearer your_admin_token_here" \
    -H "Accept: application/json"

##Desactiver un unitilisateur en donnant les raisons:

curl -X PUT "http://localhost:8000/users/deactivate/{user_id}" \
    -H "Authorization: Bearer ${ADMIN_TOKEN}" \
    -H "Content-Type: application/json" \
    -d '{"reason": "Inappropriate behavior"}'

