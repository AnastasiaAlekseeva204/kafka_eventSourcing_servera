import api from "./api";
import type { Student, StudentWithOutId } from "./types";

export const createStudent = async (student: StudentWithOutId): Promise<Student> => {
    const response = await api.post('/students/', student)
    return response.data
}

export const getAllStudents = async (): Promise<Student[]> => {
    const response = await api.get('/students/0/100') // Получаем первые 100 студентов
    return response.data
}
export const getStudent = async (id: number): Promise<Student> => {
    const response = await api.get(`/students/${id}`)
    return response.data
}
export const getStudenWithPagination = async (start: number, limit: number): Promise<Student[]> => {
    const response = await api.get(`/students/${start}/${limit}`)
    return response.data
}   
export const updateStudent = async (id: number, student: StudentWithOutId) => {
    await api.patch(`/students/${id}`, student)
}

export const getStudents = async (): Promise<Student[]> => {
    const response = await api.get('/students/0/100') // Получаем первые 100 студентов
    return response.data
}

export const deleteStudent = async (id: number) => {
    await api.delete(`/students/${id}`)
}
