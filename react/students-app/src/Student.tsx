import { Card, CardContent, Typography, Box, CardActions, Button } from "@mui/material";
import type { Student } from "./types";

interface StudentProps {
    student: Student;
    onDelete: (student: Student) => void;
    onUpdate: (student: Student) => void; //это функция, которая принимает студента и ничего не возращает, поэтому мы и пишем войд
}

export default function Student({ student, onDelete, onUpdate }: StudentProps) {
    return (
        <Card sx={{ minWidth: 275, margin: 1 }}>
            <CardContent>
                <Typography variant="h5" component="div" gutterBottom>
                    {student.last_name}
                </Typography>
                <Box sx={{ mb: 1 }}>
                    <Typography variant="body1" color="text.secondary">
                        Имя: {student.first_name}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Отчество: {student.middle_name}
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Возраст: {student.age} лет
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Пол: {student.gender ? 'Мужской' : 'Женский'}
                    </Typography>
                </Box>
            </CardContent>
            <CardActions>
                <Button onClick={()=>onUpdate(student)}>Изменить</Button>
                <Button onClick={()=>onDelete(student)}>Удалить</Button>
            </CardActions>
        </Card>
    );
}