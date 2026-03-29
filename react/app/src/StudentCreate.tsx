import { useNavigate } from "react-router-dom";
import { createStudent } from "./studentsApi";
import StudentCreateAndUpdate from "./StudentCreateAndUpdate";

export default function StudentCreate() {
    //навигация
    const navigate = useNavigate()
    //обработка отправки формы создания студента
    const handleSubmit = async (_id: number | null, first_name: string, last_name: string, middle_name: string, age: number, gender: boolean) => {
        const studentData = {
            first_name,
            last_name,
            middle_name,
            age,
            gender
        }
        
        await createStudent(studentData) //вызов api
        navigate('/') //на главную
    }
    //
    return (
        <StudentCreateAndUpdate 
            idEditable={null} //означает создание
            first_name="" 
            last_name="" 
            middle_name="" 
            age="" 
            gender="" 
            onSubmit={handleSubmit}
        />
    )
}