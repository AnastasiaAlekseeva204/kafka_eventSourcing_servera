import api from "./api"
import type { Token, UserRegister, UserLogin } from "./types"

export const registerUser = async (userData: UserRegister): Promise<Token> => {
    const response = await api.post('/auth/register', userData)
    return response.data
}

export const loginUser = async (data: UserLogin): Promise<Token> => {
    const formData = new URLSearchParams();
    
    // FastAPI OAuth2 ожидает именно 'username'
    formData.append('username', data.login_name); 
    formData.append('password', data.password);

    const response = await api.post('/auth/login', formData, {
        headers: {
            // Перезаписываем глобальный JSON заголовок на Form Data
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    
    return response.data;
}











/*import api from "./api"
import type { Token, UserRegister, UserLogin } from "./types"
export const registerUser = async (data: { login_name: string, password: string }) => {
    const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

    if (!response.ok) {
        throw new Error(`Ошибка регистрации: ${response.status}`)
    }

    return response.json()
}

export const loginUser = async (data: { login_name: string, password: string }) => {
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })

    if (!response.ok) {
        throw new Error(`Ошибка входа: ${response.status}`)
    }

    return response.json()
}
*/



/*export const registerUser = async (UserRegister: UserRegister): Promise<Token> => {
    const response = await api.post('/auth/register', UserRegister)
    return response.data
}

export const loginUser = async (UserLogin: UserLogin): Promise<Token> => {
    const response = await api.post('/auth/login_name', UserLogin)
    return response.data
}
*/
