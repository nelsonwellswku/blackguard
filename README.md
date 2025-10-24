# Blackguard ♞

Generate SQL insert statements for test data.

## Usage

> TODO

## Development

### Prerequisites

* Install the [Microsoft ODBC driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server) for your platform.

### Troubleshooting

If you get the error `ImportError: libodbc.so.2: cannot open shared object file: No such file or directory`, you need to install `unixODBC`.

```
    sudo apt-get install unixodbc-dev  # Debian/Ubuntu
    sudo yum install unixODBC-devel    # RHEL/CentOS
    sudo pacman -S unixodbc            # Arch Linux
```

## License

Blackguard source files copyright 2025 Nelson Wells, licensed under the GPL v3.0 unless otherwise noted.
