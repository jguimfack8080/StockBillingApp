curl -s "http://localhost:8001/"

curl -s -X POST "http://localhost:8001/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@test.com&password=adminpassword"

curl -s -X POST "http://localhost:8001/users/" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"email":"user1@test.com","password":"userpass","role":"caissier"}'

