import {useCallback, useEffect, useState} from 'react';
import Message from '../models/Message';
import User from '../models/User';
import UserService from '../services/UserService';
import './MessageComponent.css';
import Group from '../models/Group';

interface MessageComponentProps {
  message: Message,
}

const MessageComponent: React.FC<MessageComponentProps> = (
  props
) => {
  const [sender, setSender] = useState<User>();
  const [receiver, setReceiver] = useState<Group>();
  const fetchData = useCallback(async () => {
    const senderData = await UserService.getUserFromId(
      props.message.sender_id
    ) ?? undefined;
    const receiverData = await UserService.getGroupFromId(
      props.message.receiver_group_id
    ) ?? undefined;
    setSender(senderData);
    setReceiver(receiverData);
  }, [props.message.sender_id, props.message.receiver_group_id]);
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  const isSender = UserService.getUser()?.id === sender?.id;
  const date = new Date(props.message.date);
  return (
    <div className={`message ${isSender? "sender": "receiver"}`}>
      <div className="message-content">{ props.message.content }</div>
      <div className="message-sender">{ sender?.name || '' } { sender?.first_name || '' }</div>
      <div className="message-receiver">{ receiver?.name || '' }</div>
      <div className="message-date">{ date.toLocaleString() }</div>
    </div>
  );
}

export default MessageComponent;
