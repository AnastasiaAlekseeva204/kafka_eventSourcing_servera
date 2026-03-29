export const startSession = (token: string) => {
    localStorage.setItem("TOKEN",token)
}

export const endSession = () => {
    localStorage.removeItem("TOKEN")
}

export const hasSession = ():boolean =>{
    return localStorage.getItem("TOKEN") !== null
}

export const getSessionToken = ():string|null =>{
    return localStorage.getItem("TOKEN")
}