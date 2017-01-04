
def fullname(user):
    if not user:
        return ''
    firstname = user['firstname'].capitalize()
    lastname = user['lastname'].capitalize()
    return '%s %s' % (firstname, lastname)


def testing_completion(project):
    # XXX projects.tests theneck if completed and 8 test
    num = len(project.tests)
    if num == 0:
        return 0
    done = len([test for test in project.tests if test['operational']])
    if done == 0:
        return 0
    return int(float(done) / float(num) * 100)
