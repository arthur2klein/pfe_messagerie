import {useCallback, useEffect, useState} from 'react';
import Message from '../models/Message';
import User from '../models/User';
import UserService from '../services/UserService';
import './MessageComponent.css';
import Group from '../models/Group';

interface MessageComponentProps {
  message: Message,
  group_id: string,
}

const MessageComponent: React.FC<MessageComponentProps> = (
  props
) => {

  const [sender, setSender] = useState<User>();
  const [receiver, setReceiver] = useState<Group>();
  const [decrypted, setDecrypted] = useState<string>('');

  const fetchData = useCallback(async () => {
    const senderData = await UserService.getUserFromId(
      props.message.sender_id
    ) ?? undefined;
    const receiverData = await UserService.getGroupFromId(
      props.message.receiver_group_id
    ) ?? undefined;
    setSender(senderData);
    setReceiver(receiverData);
    // const message_decrypted = await Encryption.decrypt(
    //   props.message.content,
    //   UserService.currentUser!.id,
    //   props.group_id
    // );
    setDecrypted(props.message.content);
  }, [
    props.message.sender_id,
    props.message.receiver_group_id,
    props.message.content,
    props.group_id
  ]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const isSender = UserService.getUser()?.id === props.message.sender_id;
  const date = new Date(props.message.date);

  return sender? (
    <div className={`message ${isSender? "sender": "receiver"}`}>
      <div className="message-content">{ decrypted }</div>
      <div className="message-sender">{ sender?.name || '' } { sender?.first_name || '' }</div>
      <div className="message-receiver">{ receiver?.name || '' }</div>
      <div className="message-date">{ date.toLocaleString() }</div>
    </div>
  ): null;
}

export default MessageComponent;
