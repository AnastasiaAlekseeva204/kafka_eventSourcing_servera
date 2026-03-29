import { Box, TextField, Button, Typography, FormControl, InputLabel, Select, MenuItem, Container, Alert } from "@mui/material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { endSession } from "./session";

export interface StudentCreateAndUpdateProps{
    idEditable: number | null
    last_name: string
    first_name: string
    middle_name: string
    age: string
    gender: string
    onSubmit:(id: number| null, first_name: string, last_name: string, middle_name: string, age: number, gender: boolean) => Promise<void>
}


export default function StudentCreateAndUpdate(props: StudentCreateAndUpdateProps ) {
    //наподобие rememberSaveable
    // название - first_name и текущее состояние
    //для чего используется setfirstname - функция для обновления состояния
    const [first_name, setFirstName] = useState(props.first_name) 
    const [last_name, setLastName] = useState(props.last_name)
    const [middle_name, setMiddleName] = useState(props.middle_name)
    const [age, setAge] = useState(props.age)
    const [gender, setGender] = useState(props.gender)
    const navigate = useNavigate()
    const [error, setError] = useState('')
    const [loading, setLoading] = useState<boolean>(false)
    
    const createUpdateStudentWithTry = async () => {
        setLoading(true)
        setError('')
        
        //console.log('Отправка данных:', { first_name, last_name, middle_name, age, gender })
        
        try {
            await props.onSubmit(props.idEditable, first_name, last_name, middle_name, parseInt(age), gender === 'Мужской')
            setLoading(false)
            navigate("/students")
            // Переход на главную с перезагрузкой
            window.location.href = '/'
        }
        catch(error) {
            console.error('Ошибка создания:', error)
            const errorMessage = error instanceof Error ? error.message : 'Неизвестная ошибка'
            setError(`Ошибка: ${errorMessage}`)
            setLoading(false)
        }
    }
    //Эта функция обрабатывает отправку HTML-формы.
    //e - объект события отправки формы
    //React.FormEvent - тип события для форм в React
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault() // отменяет это стандартное поведение,позволяет обработать отправку
        createUpdateStudentWithTry()
    }
    
    
    //Условный рендеринг - показывает красное уведомление об ошибке, если error не пустой.
    //Все поля блокируются (disabled={loading}) во время отправки, предотвращает повторную отправку

    return (
        <>
            {error && <Alert severity="error">{error}</Alert>}
            <Container maxWidth="sm">
            <Box sx={{ mt: 3, mb: 2 }}>
                <Button onClick={() => navigate(-1)} variant="outlined">
                    Назад
                </Button>
                <Button onClick={() => { endSession(); navigate('/'); }} variant="contained" sx={{ ml: 2 }}>
                    Выход
                </Button>
            </Box>
            
            <Typography variant="h4" component="h1" gutterBottom>
                Создание студента
            </Typography>
            
            <Box 
                component="form" 
                onSubmit={handleSubmit}
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    gap: 2,
                    mt: 2
                }}
            >
                <TextField 
                    label="Фамилия"
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                    fullWidth
                    required
                    disabled = {loading}
                />
                <TextField
                    label="Имя"
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                    fullWidth
                    required
                    disabled = {loading}
                />
                <TextField
                    label="Отчество"
                    value={middle_name}
                    onChange={(e) => setMiddleName(e.target.value)}
                    fullWidth
                    disabled = {loading}
                />
                <TextField
                    label="Возраст"
                    type="number"
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                    fullWidth
                    required //необязательное поле
                    inputProps={{ min: 16, max: 100 }} //минимальный возраст для ввода в форму
                    disabled = {loading}
                />
                <FormControl fullWidth required>
                    <InputLabel>Пол</InputLabel>
                    <Select
                        value={gender}
                        label="Пол"
                        onChange={(e) => setGender(e.target.value)}
                        disabled = {loading}
                    >
                        <MenuItem value="Мужской">Мужской</MenuItem>
                        <MenuItem value="Женский">Женский</MenuItem>
                    </Select>
                </FormControl>
                
                <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
                    <Button 
                        type="submit"
                        variant="contained" 
                        color="primary"
                        fullWidth
                        disabled = {loading}

                    >
                        {props.idEditable? "Создать" : "Изменить"}
                    </Button>
                    <Button 
                        variant="outlined" 
                        color="secondary"
                        fullWidth
                        onClick={() => navigate(-1)}
                        disabled = {loading}
                    >
                        Отмена
                    </Button>
                </Box>
            </Box>
            </Container>
        </>
    )
}