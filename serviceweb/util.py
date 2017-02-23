
def fullname(user):
    """ Returns the full name of a user.
    """
    if not user:
        return ''
    firstname = user['firstname'].capitalize()
    lastname = user['lastname'].capitalize()
    return '%s %s' % (firstname, lastname)


def testing_completion(project):
    """Returns a completion percentage for a project.

    e.g. the percentage of tests that are marked operational
    """
    num = len(project.tests)
    if num == 0:
        return 0
    done = len([test for test in project.tests if test['operational']])
    if done == 0:
        return 0
    return int(float(done) / float(num) * 100)
