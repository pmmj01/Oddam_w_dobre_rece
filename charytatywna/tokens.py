from django.contrib.auth.tokens import default_token_generator

# Tworzenie tokenu dla aktywacji konta
account_activation_token = default_token_generator.make_token(user)

# Sprawdzanie ważności tokenu
is_valid = default_token_generator.check_token(user, token)
