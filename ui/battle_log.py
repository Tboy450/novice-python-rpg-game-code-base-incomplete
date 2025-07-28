# Battle log management extracted from BattleScreen class


def add_log(self, message):
    """
    Adds a message to the battle log and sets the waiting_for_continue flag.
    Args:
        message (str): The message to display in the battle log.
    """
    self.battle_log.append(message)
    self.waiting_for_continue = True

# (Add any additional log formatting or paging helpers here as needed) 