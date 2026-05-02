import { createContext, useState, useEffect, useContext } from "react";

const AuthContext = createContext()

export function AuthProvider({children}){

    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {

        const access = localStorage.getItem('access')
        const role = localStorage.getItem('role')
        if(access && role){
            fetchUser(access, role)
        } else{
            setLoading(false)
        }

    },[])

    async function fetchUser(token, role){
        try{
            
            const role = localStorage.getItem('role')
            const endpoint = role === 'mentor'
            ? 'http://127.0.0.1:8000/api/mentor/profile/'
            : 'http://127.0.0.1:8000/api/career-gaper/profile/'

            const response = await fetch(endpoint, {
                headers:{
                    'Authorization': `Bearer ${token}`
                }
            })

            if (response.ok){
                const data = await response.json()
                setUser({...data, role})
            }
            else{
                localStorage.removeItem('access')
                localStorage.removeItem('refresh')
                localStorage.removeItem('role')
                localStorage.removeItem('name')
            }
        }catch (err){
            console.log("Error fetching user:", err)
        }finally{
            setLoading(false)
        }
        
    }
    

    function logout(){
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')
        localStorage.removeItem('role')
        localStorage.removeItem('name')
        setUser(null)
    }

    return(
        <AuthContext.Provider value={{user, setUser, loading, logout}}>
            {children}
        </AuthContext.Provider>
    )

}

export function useAuth(){
    return useContext(AuthContext)
}