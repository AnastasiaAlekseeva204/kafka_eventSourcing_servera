import { loginUser, registerUser } from "./auth_internal"
import { startSession } from "./session"

export const register = async(login_name: string, password: string)=>{
    const response = await registerUser({login_name, password}) as any
    // Исправлено: используем access_token
        startSession(response.access_token)
}

export const login = async(login_name: string, password: string) => {
    const response = await loginUser({login_name, password}) as any; // Приведение к any
    startSession(response.access_token);
}