export interface User {
    userId: number | null;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    password: string | null;
}

export interface Credentials {
    email: string;
    password: string;
}