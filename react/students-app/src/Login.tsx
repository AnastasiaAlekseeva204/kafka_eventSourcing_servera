import { Link } from "react-router-dom";
import { login } from "./auth";
import LoginAndRegister from "./LoginAndRegister";
export default function Login(){
    return<>
    <h1>Вход</h1>
    <LoginAndRegister buttonText="Войти" onSubmit={login}></LoginAndRegister>
        <Link to={"/register"}></Link>
    </>
}