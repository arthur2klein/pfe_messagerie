interface User {
  id: string,
  name: string,
  first_name: string,
  email: string,
  join_date: number,
  auth_id: string
}

class UserService {
  
  private static testUser: User = {
    id: '1',
    name: 'doe',
    first_name: 'john',
    email: 'e@mail.com',
    join_date: 1000,
    auth_id: '0',
  }

  private static currentUser: User | undefined = this.testUser;

  static isConnected(): boolean {
    return this.currentUser !== undefined;
  }

  static getUser(): User | undefined {
    return this.currentUser;
  }
}

export default UserService;
