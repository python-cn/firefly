# coding=utf-8

KEYBOARD_URL_MAPS = {
    'default': [
        [
            'Site wide shortcuts',  # keyboard category
            [
                # ('keyboard shortcut', 'keyboard info')
                ('s', 'Focus search bar'),
                ('g n', 'Go to Notifications'),
                ('g h', 'Go to personal page'),
                ('?', 'Bring up this help dialog'),
            ],
        ],
        [
            'Registration and login',
            [
                ('l r', 'Open register window'),
                ('l o', 'Open login window'),
                ('l t', 'Logout'),
                ('l c', 'Close register/login window'),
            ],
        ],
        [
            'Notifications',
            [
                ('e / I / y', 'Mark as read'),
            ],
        ],
        [
            'Personal page',
            [
                ('g s', 'Go to personal settings page'),
                ('g t', 'Go to personal topic page'),
            ]
        ]
    ],
    '/': [
        [
            'Topic list shortcuts',
            [
                ('j', 'Move selection down'),
                ('k', 'Move selection up'),
                ('o', 'Open selection'),
            ],
        ],
        [
            'Create Topic',
            [
                ('t o', 'Open create topic window'),
                ('t q', 'Close create topic window'),
                ('t s', 'Submit create topic'),
            ],
        ]
    ],
    '/post': [
        [
            'Reply Topic',
            [
                ('p o', 'Open reply topic window'),
                ('p q', 'Close reply topic window'),
                ('p s', 'Submit reply topic'),
            ],
        ],
    ]
}
