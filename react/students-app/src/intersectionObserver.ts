import { useEffect } from "react"
import { useState, type RefObject } from "react"
// внедрить Intersectio чтобы понимать когда грузить слд студенты
export interface IntersectionObserverOptions {
    treshold: number,
    rootMargin: string,
}

export const useIntersectionObserver = (
    elementRef : RefObject<Element | null>, //ссылка на отслеживаемый элемент
    option: IntersectionObserverOptions = {} as IntersectionObserverOptions //опция наблюдателя
): boolean => {
    const [isIntersecting, setIsIntersecting] = useState(false)

    useEffect(() => {
        if(!elementRef.current) return //проверка существования элемента

        const observer = new IntersectionObserver(
            ([entry]) => {
                setIsIntersecting(entry.isIntersecting)  //обновление состояния
            },
            {
                threshold: option.treshold || 0, //порог срабатывания
                rootMargin: option.rootMargin || '0px',//отсупы
            }
        )

        observer.observe(elementRef.current) //начало наблюдения

        return () => {
            observer.disconnect() //отчистка ресурсов
        }
    }, [elementRef, option.rootMargin, option.treshold])
//возращаем значение
    if(isIntersecting) return true
    return false
}