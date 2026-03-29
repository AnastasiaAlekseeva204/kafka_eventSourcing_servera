import { createBrowserRouter } from "react-router-dom";
import App from "./App";
import Students from "./Students";
import StudentCreate from "./StudentCreate";
import StudentEdit from "./StudentEdit";
import Login from "./Login";
import Register from "./Register";
import { ProtectedRoute } from "./ProtectedRoute";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />, //главный контейнер
    children: [
        {
        index: true, //index.html когда написан индекс тру от не написанного
        //если как у меня, то он отображает путь, когда точно совпадает с родительским (/) и не добавляет дополнительных сегментов к ссылке
        //Без index: true (обычный маршрут): у него ссылка сразу родитель+ свой сегмент и показывается при переходе /students
        // Итог: Обычный маршрут создает новый URL-путь, а index: true использует URL родителя.
        element: <Login />     // Отображает путь возращения к логину
        },
        {
        path: "login",
        element: <Login />     // Отображает путь к логину
        },
        {
        path: "register",
        element: <Register />     // Отображает путь обратно к регистрации
        },
        {
            path: "students",
            element: <ProtectedRoute/>,
            children: [
                // ... вложенные маршруты для студентов ...
                {
                   index: true,
                   element: <Students />
                },
            {
                path: 'create',
                element: <StudentCreate /> // Отображается, когда путь="/students/create"
            },
            {
                path: ':id/edit', //:id — это динамический параметр
                element: <StudentEdit /> // Отображается, когда путь="/students/123/edit"
            }
            ]
        }
    ]
  },
])