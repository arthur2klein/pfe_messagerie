set -e

mkdir -p /var/log/postgresql
chown -R postgres:postgres /var/log/postgresql
touch /var/log/postgresql/postgresql.log
chown postgres:postgres /var/log/postgresql/postgresql.log

