set -e

# Create the log directory
mkdir -p /var/log/postgresql
chown -R postgres:postgres /var/log/postgresql
