import { useState } from "react";
import type { Student } from "./types";
import { deleteStudent, getAllStudents } from "./studentsApi";

//Partial - необязательнные поля |null
interface StudentState{
    students: Student[]
    loading: boolean
    error: string | null
    successMessage: string | null
}


interface StudentHook{
    loadStudents: () => Promise<void>,
    deleteStudent: (student:Student) => Promise<void>,
    refreshStudents: () => Promise<void>,
    state: StudentState
}

export const useStudents = (): StudentHook => {
    const [state, setState] = useState<StudentState>({
        students: [],
        loading: false,
        error: null,
        successMessage: null
    })
    //... - это обращение к экземплярам интерфейса, что у нас хранится interface StudentState
    const loadStudents = async () => {
        console.log('Начало загрузки студентов...')
        setState(prev => ({...prev, loading: true, error: null}))
        try{
            const students = await getAllStudents()
            console.log('Получено студентов:', students.length, students)
            setState(prev => ({...prev, students, loading: false, error: null}))
        }
        catch(error){
            console.error('Ошибка загрузки:', error)
            const errorMessage = error instanceof Error ? error.message : 'Unknown error'
            setState(prev => ({...prev, loading: false, error: errorMessage}))
        }
    }
    const deleteStudentInHook  = async (student:Student) => {
        setState(prev => ({...prev, students: prev.students.filter(s => s.id !== student.id)}))
        try{
            await deleteStudent(student.id)
            setState(prev => ({...prev, successMessage:'Успешно удален студент'}))
        }
        catch(error){
            const errorMessage = error instanceof Error ? error.message : 'Unknown error'
            setState(prev => ({...prev, error: errorMessage, students:[...prev.students,student]}))
        }
    }
    return{
        loadStudents,
        state, 
        deleteStudent: deleteStudentInHook,
        refreshStudents: loadStudents
    }
}