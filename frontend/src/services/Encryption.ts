import {createMessage, decrypt, encrypt, generateKey, readKey, readPrivateKey} from 'openpgp';
import UserService from './UserService';

class Encryption {

  static async encrypt(
    message: string,
    user_id: string,
    group_id: string
  ): Promise<string> {
    const publicKey = await Encryption.getPublicKey(user_id, group_id);
    if (publicKey === null) {
      return '';
    }
    const key = await readKey({armoredKey: publicKey});
    const encryptedMessage = await encrypt({
      message: await createMessage({text: message}),
      encryptionKeys: key,
    });
    return encryptedMessage.toString();
  }

  static async decrypt(
    message: string,
    user_id: string,
    group_id: string
  ): Promise<string> {
    const privateKey = await Encryption.getPrivateKey(user_id, group_id);
    console.log(privateKey);
    if (privateKey === null) {
      return '';
    }
    const key = await readPrivateKey({armoredKey: privateKey});
    const { data: decrypted } = await decrypt({
      message: await createMessage({text: message}),
      decryptionKeys: key,
    });
    return decrypted.toString();
  }

  static async createKey(group_id: string, user_id: string): Promise<any> {
    const {privateKey, publicKey} = await generateKey({
      type: 'ecc',
      curve: 'curve25519',
      userIDs: [{ name: `${group_id} ${user_id}`}]
    });
    Encryption.storePublicKey(user_id, group_id, publicKey);
    Encryption.storePrivateKey(user_id, group_id, privateKey);
    return {privateKey, publicKey};
  }

  static storePrivateKey(user_id: string, group_id: string, key: string) {
    UserService.storePrivateKey(user_id, group_id, key);
  }

  static storePublicKey(user_id: string, group_id: string, key: string) {
    UserService.storePublicKey(user_id, group_id, key);
  }

  static async getPrivateKey(user_id: string, group_id: string): Promise<string | null> {
    if (UserService.currentUser?.id !== user_id) return null;
    return await UserService.getPrivateKey(user_id, group_id);
  }

  static async getPublicKey(user_id: string, group_id: string): Promise<string | null> {
    const groupMembers = await UserService.getUserGroup(group_id);
    const idMembers = groupMembers.map((user) => user.id);
    if (idMembers.indexOf(UserService.currentUser!.id) === -1) return null;
    return await UserService.getPublicKey(user_id, group_id);
  }
}

export default Encryption;
