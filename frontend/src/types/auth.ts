export type UserCreate = {
  email: string;
  password: string;
};

export type TokenResponse = {
  access_token: string;
  token_type?: string;
};

export type User = {
  id?: string | number;
  email: string;
};
export interface UserCreate {
  email: string;
  password: string;
}
