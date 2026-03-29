import api from './api'
import { useEffect, useRef } from 'react'
import { useStudents } from './useStudents.ts'
import Student from './Student'
import { Box, Button, CircularProgress, Skeleton, Typography } from '@mui/material'
import type { Student as StudentType } from './types'
import { useNavigate, useLocation } from 'react-router-dom'
import { useInfiniteQuery } from '@tanstack/react-query'
import { useIntersectionObserver } from './intersectionObserver.ts'
import { endSession } from './session.ts'

export default function Students() {
    const { state, loadStudents, deleteStudent } = useStudents()
    const navigate = useNavigate()
    const location = useLocation()
    const loadMoreRef = useRef<Element>(null)
    
    useEffect(() => {
        loadStudents()
    }, [])
    
    useEffect(() => {
        // Перезагружаем данные при каждом возврате
        loadStudents()
    }, [location])
    
    const handleDelete = (student: StudentType) => {
        deleteStudent(student)
    }
    const handleUpdate = (student: StudentType) => {
        navigate(`/students/${student.id}/edit`)
    }
    //getNextPageParam - определяет есть ли следующая страница
    //Если последняя страница содержит 30 элементов, значит есть еще данные
    //pageParam * LIMIT вычисляет offset для API
    
            const LIMIT = 30;
    const { 
        data, 
        fetchNextPage, 
        hasNextPage, 
        isFetchingNextPage, 
        error: queryError 
    } = useInfiniteQuery({
        queryKey: ['paginatedStudents'], 
        initialPageParam: 0,
        queryFn: (context) => {
            const page = context.pageParam as number;
            return getStudentWithPagination({ 
                pageParam: page * LIMIT, 
                limit: LIMIT 
            });
        },
        getNextPageParam: (lastPage) => {
            return lastPage.length === LIMIT ? lastPage.length : undefined;
        },
        staleTime: 30000
    });
    
    //flat преобразует все списки/массивы в один список 
    const allStudents = data?.pages.flat() || []
    
    const isIntersection = useIntersectionObserver(loadMoreRef, { treshold: 0.1,  //Срабатывает при 10% видимости
        rootMargin: '100px' }) ///Срабатывает за 100px до появления
    
    // Автоматическая загрузка при пересечении
    useEffect(() => {
        if (isIntersection && hasNextPage && !isFetchingNextPage) {
            fetchNextPage()
        }
    }, [isIntersection, hasNextPage, isFetchingNextPage, fetchNextPage])
    
    //Skeleton это компонент для загрузки (из Material-UI, который показывает анимированную заглушку (placeholder) во время загрузки данных.)
    return (
        <>
            <Box sx={{ mb: 2, display: 'flex', gap: 2 }}>
                <Button onClick={() => navigate('/students/create')} variant="contained">
                    Создать студента
                </Button>
                <Button onClick={() => loadStudents()} variant="outlined">
                    Обновить список
                </Button>
                <Button onClick={() => { endSession(); navigate('/'); }} variant="contained">
                    Выход
                </Button>
            </Box>
            <Box display='flex' flexWrap='wrap'>
                {state.loading && <Skeleton width={600} height={20} variant='text' />} 
                {state.error && <Typography color="error">{state.error}</Typography>}
                {queryError && <Typography color="error">{queryError.message}</Typography>}
                {allStudents.map((student) => (
                    <Student 
                        key={student.id} 
                        student={student} 
                        onDelete={handleDelete}
                        onUpdate={handleUpdate}
                    />
                ))}
                {hasNextPage && 
                (isFetchingNextPage ? (<CircularProgress/>) : (
                    <div ref={loadMoreRef as React.RefObject<HTMLDivElement>}>
                        <Button onClick={() => fetchNextPage()}>Загрузить ещё</Button>
                    </div>
                ))
                }
                {!hasNextPage && <div>Больше студентов нет</div>}
            </Box>
        </>
    )
}

async function getStudentWithPagination({ pageParam, limit }: { pageParam: number, limit: number }) {
    // Используем наш axios экземпляр 'api', который уже содержит токен!
    const response = await api.get(`/students/${pageParam}/${limit}`);
    return response.data;
}