def user_in_db(user_id: int, all_users_data: list) -> bool:
    if (user_id,) in all_users_data:
        return True
    else:
        return False
