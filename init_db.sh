user="60201_user"
db="BE_60201"

docker exec -it 4d9e93138f59 sh -c "mysql -proot -e 'create database ${db}; CREATE USER \"${user}\"@\"localhost\" IDENTIFIED BY \"60201_password\"; GRANT ALL PRIVILEGES ON ${db}.* TO \"${user}\"@\"localhost\";' && mysql -u${user} -p60201_password -e 'use ${db}; source prestashop.sql;'"