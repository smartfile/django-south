from traceback import format_exception

class SouthError(RuntimeError):
    pass


class BrokenMigration(SouthError):
    def __init__(self, migration, exc_info):
        self.migration = migration
        self.exc_info = exc_info
        self.traceback = ''

    def __str__(self):
        if self.exc_info:
            self.traceback = ''.join(format_exception(*self.exc_info))
        return ("While loading migration '%s':\n"
                '%(traceback)s' % self.__dict__)


class UnknownMigration(BrokenMigration):
    def __str__(self):
        return ("Migration '%(migration)s' probably doesn't exist.\n"
                '%(traceback)s' % self.__dict__)


class NoMigrations(SouthError):
    def __init__(self, application):
        self.application = application

    def __str__(self):
        return "Application '%(application)s' has no migrations." % self.__dict__


class GuessMigrationError(SouthError):
    def __init__(self, prefix, matches):
        self.prefix = prefix
        self.matches = matches

    def __str__(self):
        self.matches_list = "\n     ".join(self.matches)
        return ("Prefix '%(prefix)s' matches more than one migration:\n"
                "     %(matches_list)") % self.__dict__


class DependsOnHigherMigration(SouthError):
    def __init__(self, migration, depends_on):
        self.migration = migration
        self.depends_on = depends_on

    def __str__(self):
        return "Lower migration '%(migration)s' depends on a higher migration '%(depends_on)s' in the same app." % self.__dict__


class DependsOnUnknownMigration(SouthError):
    def __init__(self, migration, depends_on):
        self.migration = migration
        self.depends_on = depends_on

    def __str__(self):
        print "Migration '%(migration)s' depends on unknown migration '%(depends_on)s'." % self.__dict__


class DependsOnUnmigratedApplication(SouthError):
    def __init__(self, migration, application):
        self.migration = migration
        self.application = application

    def __str__(self):
        return "Migration '%(migration)s' depends on unmigrated application '%(application)s'." % self.__dict__


