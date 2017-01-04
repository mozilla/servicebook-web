
def fullname(user):
    if not user:
        return ''
    firstname = user['firstname'].capitalize()
    lastname = user['lastname'].capitalize()
    return '%s %s' % (firstname, lastname)


def testing_completion(project):
    # XXX projects.tests theneck if completed and 8 test
    return 75
