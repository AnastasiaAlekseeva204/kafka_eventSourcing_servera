import { register } from "./auth";
import LoginAndRegister from "./LoginAndRegister";
export default function Register(){


    return<>
    <h1>Регистрация</h1>
    <LoginAndRegister buttonText="Зарегистрироваться" onSubmit={register}></LoginAndRegister>
    </>
}
