export interface User {
  id: string;
  email: string;
  name: string;
  emailVerified: boolean;
  image?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Session {
  user: User;
  session: {
    token: string;
    expiresAt: string;
  };
}
