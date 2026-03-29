import React, { useState } from "react";
import StudentCreateAndUpdate from "./StudentCreateAndUpdate";
import { updateStudent, getStudent } from "./studentsApi";
import { useNavigate, useParams } from "react-router-dom";

export default function StudentEdit() {
    const { id: idParam } = useParams<{ id: string }>()
    const [loading, setLoading] = useState(true)
    const [first_name, setFirstName] = useState('')
    const [last_name, setLastName] = useState('')
    const [middle_name, setMiddleName] = useState('')
    const [age, setAge] = useState('')
    const [gender, setGender] = useState('')
    const [studentId, setStudentId] = useState(0)
    const [error, setError] = useState('')

    const loadStudent = async (id: number) => {
        try {
            const student = await getStudent(id)
            setLoading(false)
            setFirstName(student.first_name)
            setLastName(student.last_name)
            setMiddleName(student.middle_name)
            setAge(student.age.toString())
            setGender(student.gender ? 'Мужской' : 'Женский')
            setStudentId(student.id)
        }
        catch(error) {
            const errorMessage = error instanceof Error ? error.message : 'Неизвестная ошибка'
            setLoading(false)
            setError(errorMessage)
        }
    }

    // Загружаем студента при монтировании
    React.useEffect(() => {
        if (idParam) {
            const idInt = parseInt(idParam)
            if (!isNaN(idInt)) {
                loadStudent(idInt)
            } else {
                setError('Некорректный ID')
                setLoading(false)
            }
        } else {
            setError('ID не найден')
            setLoading(false)
        }
    }, [idParam])
    const navigate = useNavigate()
    
    const handleSubmit = async (id: number | null, first_name: string, last_name: string, middle_name: string, age: number, gender: boolean) => {
        if (studentId) {
            await updateStudent(studentId, {
                first_name,
                last_name,
                middle_name,
                age,
                gender
            })
        }
        navigate('/')
    }
    
    if (loading) {
        return <div>Загрузка...</div>
    }
    
    if (error) {
        return <div>Ошибка: {error}</div>
    }
    
    return (
        <StudentCreateAndUpdate 
            idEditable={studentId} 
            first_name={first_name} 
            last_name={last_name} 
            middle_name={middle_name} 
            age={age} 
            gender={gender} 
            onSubmit={handleSubmit}
        />
    )
}