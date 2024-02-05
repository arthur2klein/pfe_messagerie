from shared.models.message import Message
from shared.servies.db_service import Db_service

class Message_iterator:
    """ Iterator over the list of message of a given group.
    ---
    Attributes:
        group_id (str): Id of the group we iterate over.
        current_message (Optional[Message]): Message the iterator is currently
        at.
    ---
    Methods:
        __iter__(Self, str): Create a new iterator for the given group.
        __next__(Self) -> Message: Advance the iterator to the next message.
    """

    def __iter__(self: Self, group_id: str, db_access: Db_service) -> Self:
        """ Creates a new iterator for the given group.
        ---
        Parameters:
            self (Self): Current instance.
            group_id (str): Id of the group from which we will get the messages.
            db_service (Db_service): Service that access to the database.
        ---
        Returns:
            (Self): Current instance.
        ---
        Example:
        ```python
        new_iterator = Message_iterator('5')
        ```
        """
        self.group_id = group_id
        self.db_access = db_access
        try:
            self.current_message = self.db_access.iter_message_first(group_id)
        except ValueError as err:
            raise ValueError(
                    f'Could not create the iterator for {self.group_id}: {err}'
                    )
        return self

    def __next__(self: Self) -> Message:
        """ Advance to the next message of the group.
        ---
        Parameters:
            self (Self): Current instance.
        ---
        Returns:
            (Message): Next message of the group.
        ---
        Example:
        ```python
        new_iterator = Message_iterator('5')
        next_message = new_iterator.next()
        ```
        """
        try:
            res = self.current_message
            self.current_message = self.db_access.iter_message_next(
                    self.current_message
                    )
            return res
        except StopIteration:
            raise StopIteration
        except ValueError as err:
            raise ValueError(
                    f'Could not create the iterator for {self.group_id}: {err}'
                    )
