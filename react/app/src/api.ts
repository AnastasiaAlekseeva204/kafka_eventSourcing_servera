import axios, { type AxiosResponse, type InternalAxiosRequestConfig } from "axios";
import { endSession, getSessionToken } from "./session";

const api = axios.create({baseURL: "http://127.0.0.1:8000/api",
    timeout:10000,
    headers:{'Content-Type': 'application/json',}})

api.interceptors.request.use((value: InternalAxiosRequestConfig) => {
   const token = getSessionToken()
   if(token !=null){
    value.headers.Authorization = `Bearer ${token}`
   }
    return value
})
api.interceptors.response.use((value: AxiosResponse) =>{
    return value
    },
    (error) =>{
        if(error.response && error.response.status === 401){
            endSession()
            window.location.href = "/login"
        }
        return Promise.reject(error)
    }
)

export default api

//способ подключения 
//const api = axios.create({...}):  создаем собственную служебную машину этой службы, но со стандартными настройками
//1^11 08/12