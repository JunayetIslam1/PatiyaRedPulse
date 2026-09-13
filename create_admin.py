#!/usr/bin/env python
"""
Creates the first Django superuser from environment variables.

No account or password is hard-coded in this script — nothing here should
ever ship with a default/demo login. Set the following before running it:

    ADMIN_USERNAME   (required)
    ADMIN_EMAIL      (required)
    ADMIN_PASSWORD   (required, must pass Django's password validators)

Example:
    ADMIN_USERNAME=youradmin ADMIN_EMAIL=you@example.com ADMIN_PASSWORD='a-strong-unique-password' \
        python create_admin.py

On most setups the built-in, interactive command works just as well and
never needs an environment variable at all:
    python manage.py createsuperuser
"""
import os
import sys

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patiya_redpulse.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


def main():
    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')

    missing = [name for name, value in (
        ('ADMIN_USERNAME', username),
        ('ADMIN_EMAIL', email),
        ('ADMIN_PASSWORD', password),
    ) if not value]

    if missing:
        print('Missing required environment variable(s): ' + ', '.join(missing))
        print('Set ADMIN_USERNAME, ADMIN_EMAIL and ADMIN_PASSWORD, or just run:')
        print('    python manage.py createsuperuser')
        sys.exit(1)

    if User.objects.filter(username=username).exists():
        print(f'A user named "{username}" already exists. No changes made.')
        sys.exit(0)

    try:
        validate_password(password)
    except ValidationError as exc:
        print('ADMIN_PASSWORD is too weak:')
        for error in exc.messages:
            print(f'  - {error}')
        sys.exit(1)

    User.objects.create_superuser(username, email, password)
    print(f'Superuser "{username}" created successfully. Please log in and, if this '
          f'was set via a shared/temporary value, rotate the password immediately.')


if __name__ == '__main__':
    main()
