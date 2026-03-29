//ts = tipeScript 
// Omit - удаление полей
//Pick - получение полей
//Partial - необязательнные поля |null
//Required - обязательнные поля

export interface Student {
    id: number;
    last_name: string;
    first_name: string;
    middle_name: string;
    gender: boolean;
    age: number
}

export type StudentWithOutId = Omit<Student, 'id'>

export interface UserLogin{
    login_name: string
    password: string
}

export type UserRegister = UserLogin

export interface Token {
    access_token: string;
    token_type: string;
}