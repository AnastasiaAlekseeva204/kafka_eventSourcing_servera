import { TextField } from "@mui/material";
import Box from "@mui/material/Box";
import { useState } from "react";
import { endSession, hasSession } from "./session";
import { useNavigate } from "react-router-dom";

export interface LoginAndRegisterProps{
    onSubmit: (login_name: string, password: string)=>Promise<void>
    buttonText: string
}

export default function LoginAndRegister({onSubmit, buttonText}: LoginAndRegisterProps){

    const [login_name, setLoginName] = useState("")
    const [password, setPassword] = useState("")
    const [loading,setLoading] = useState(false)
    const [error, setError] = useState("")
    const navigate = useNavigate()

const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
        setError("");
        // Очищаем старую сессию перед новым входом
        endSession(); 
        
        // Предположим, onSubmit возвращает объект с токеном
        // Если ваш onSubmit ничего не возвращает, а делает всё внутри - проверьте файл auth.ts
        await onSubmit(login_name, password);
        
        // Проверяем сессию СРАЗУ после завершения onSubmit
        if (hasSession()) {
            navigate("/students");
        } else {
            setError("Ошибка: Сессия не была создана. Проверьте сохранение токена.");
        }
    } catch (err) {
        console.error('Ошибка:', err);
        setError(`Ошибка аутентификации: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`);
    } finally {
        setLoading(false);
    }

   /* const handleSubmit = async(e: React.FormEvent)=>{
        e.preventDefault()
        setLoading(true)
        try{
            setError("")
            endSession()
            await onSubmit(login_name, password)
        } catch (err){
           console.error('Ошибка:', err)
           setError(`Ошибка аутентификации: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`)
        }
        
        finally {
            setLoading(false)
        }
        if (hasSession()){
            navigate("/students")
        }*/
    }
    return<>

        <div>{error}</div>
        <Box component="form" onSubmit={handleSubmit}>
            <TextField
            label="login_name"
            value={login_name}
            disabled={loading}
            onChange={(e)=> setLoginName(e.target.value)}
            />
            <TextField 
            label="password"
            value={password}
            disabled={loading}
            onChange={(e)=> setPassword(e.target.value)}
            type="password"
            />
            <button type="submit" disabled={loading}>
                {buttonText}
            </button>
        </Box>
    </>
}
