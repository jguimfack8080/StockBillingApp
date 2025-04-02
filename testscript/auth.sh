curl -s "http://localhost:8001/"

curl -s -X POST "http://localhost:8001/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@test.com&password=adminpassword"

curl -X POST "http://localhost:8001/users/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMUB0ZXN0LmNvbSIsInJvbGUiOiJtYW5hZ2VyIiwiZXhwIjoxNzQzNjMzMDg5fQ.ZvEt7mM3z9Zh7WA2W9P_wr22DnzyFpW0XMG35l3E_Hc" \
     -d '{
           "first_name": "Jean",
           "last_name": "Dupont",
           "birth_date": "1995-05-20",
           "id_card_number": "1234567890",
           "email": "jean.dupont@example.com",
           "password": "password123",
           "role": "manager"
         }'
