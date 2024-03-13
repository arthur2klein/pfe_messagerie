import openpgp from 'openpgp';
import {generateKey} from 'openpgp/lightweight';
import User from '../models/User';
import Group from '../models/Group';
import UserService from './UserService';

class Encryption {
  static async encrypt(
    message: string,
    publickey: string
  ): Promise<string> {
    const key = await openpgp.readKey({armoredKey: publickey});
    const encryptedMessage = await openpgp.encrypt({
      message: await openpgp.createMessage({text: message}),
      encryptionKeys: key,
    });
    return encryptedMessage.toString();
  }

  static async decrypt(message: string, privatekey: string): Promise<string> {
    const key = await openpgp.readPrivateKey({armoredKey: privatekey});
    const { data: decrypted, signatures } = await openpgp.decrypt({
      message: await openpgp.createMessage({text: message}),
      decryptionKeys: key,
    });
    return decrypted.toString();
  }

  static async createKey(group: Group, user: User): Promise<any> {
    const {privateKey, publicKey} = await generateKey({
      type: 'ecc',
      curve: 'curve25519',
      userIDs: [{ name: group.name , email: user.email}]
    });
    Encryption.sharePublicKeyInGroup(user, group, publicKey);
    Encryption.storePrivateKey(user, group, privateKey);
    return {privateKey, publicKey};
  }

  static storePrivateKey(user: User, group: Group, key: string) {
    UserService.storePrivateKey(user, group, key);
  }

  static storePublicKey(user: User, group: Group, key: string) {
    UserService.storePublicKey(user, group, key);
  }

  static async getPrivateKey(user: User, group: Group): Promise<string | null> {
    if (UserService.currentUser?.id !== user.id) return null;
    return await UserService.getPrivateKey(user, group);
  }

  static async getPublicKey(user: User, group: Group): Promise<string | null> {
    if (UserService.getUserGroup()) return null;
    return await UserService.getPublicKey(user, group);
  }



}
