def generate_deferred_fields() -> list[str]:
    return [
        'user__bio',
        'user__email',
        'user__password',
        'user__is_staff',
        'user__is_active',
        'user__visibility',
        'user__last_login',
        'user__date_joined',
        'user__is_superuser',
    ]
