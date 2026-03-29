import { Navigate, Outlet } from "react-router-dom";
import { hasSession } from "./session";

export function ProtectedRoute(){
    return hasSession()?
     <Outlet/> 
     :<Navigate to="/" replace />;
}