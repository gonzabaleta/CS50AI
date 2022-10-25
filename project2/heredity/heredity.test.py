from heredity import joint_probability, PROBS

people = {
    'Harry': {
        'name': 'Harry',
        'mother': 'Lily',
        'father': 'James',
        'trait': None
    },
    'James': {
        'name': 'James',
        'mother': None,
        'father': None,
        'trait': True
    },
    'Lily': {
        'name': 'Lily',
        'mother': None,
        'father': None,
        'trait': False
    }
}

print(joint_probability(people, {"Harry"}, {"James"}, {"James"}))
