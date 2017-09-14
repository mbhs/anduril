from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

import csv
import os
import string


def generate_hashed_filename(path):
    """Given /path/to/file.txt, generate /path/to/file.hashed.txt."""

    head, tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    return os.path.join(head, ".".join((name, "hashed", extension.lstrip("."))))


def printable(handle):
    """Generator that filters non-printable characters while reading."""

    for line in handle:
        yield "".join(filter(lambda x: x in string.printable, line))


class Command(BaseCommand):
    """Hashes user passwords in a CSV dump."""

    help = """\
    This command is used to hash passwords according to Django's 
    internal system. The main argument is the CSV file of student
    information, and by default, the column with the label `password`
    will be the one replaced with hashes. This behavior can be changed
    either by selecting a different column name or index.
    """

    def add_arguments(self, parser):
        """Add arguments to the parser."""

        parser.add_argument("dump", help="the CSV file of student information.")
        parser.add_argument("-i", "--index", dest="index", type=int,
                            help="Select the password column by index.\
                            Column numbering is 1-indexed, so the first column has number 1.")
        parser.add_argument("--header", dest="header", action="store_true", default=False,
                            help="Specify if there is a header row. Important when using column index, which is the\
                            only mode that assumes there isn't a header.")
        parser.add_argument("-n", "--name", dest="name",
                            help="Select the password column by column name.")

    def handle(self, dump, *args, index=None, name=None, header=None, **kwargs):
        """Run the actual command."""

        hashed = generate_hashed_filename(dump)

        with open(dump) as read, open(hashed, "w") as write:
            reader = csv.reader(printable(read))
            writer = csv.writer(write)

            # Determine password column
            if index is not None and not header:
                index -= 1
            else:
                header = next(reader)
                writer.writerow(header)

                columns = list(map(lambda s: s.lower(), header))
                name = name or "password"
                if name not in columns:
                    print("Cannot find specified column name in CSV file!")
                    return
                index = columns.index(name)

            for line in reader:
                line[index] = make_password(line[index])
                writer.writerow(line)
