import {useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import '../App.css'

export default function Dashboard() {

    const navigate = useNavigate()
    const {user, loading, logout} = useAuth()

    useEffect(() => {
        if(!loading && !user){
            navigate('/login')
        }
    },[user, loading])

    if (loading) return <div>Loading...</div>
    if (!user) return null

    console.log(user)
    console.log(user.role)

    function handleLogout(){
        logout()
        navigate('/login')
    }

    return (
        <div>
        <div>
            {user.role === 'career_gaper' && <CareerGaperDashboard user={user}/>}
            {user.role === 'mentor' && <MentorDashboard user={user}/>}
        </div>
        <div>
            <button onClick={handleLogout}>Logout</button>
        </div>
        </div>
    )
}

function CareerGaperDashboard({user}) {
    return (
        <div>
            <h2>Welcome, {user.name} 👋</h2>
            <p>You are a Career Gaper</p>
        </div>
    )
}

function MentorDashboard({user}){
    return (
        <div>
            <h2>Welcome, {user.name} 👋</h2>
            <p>You are a Mentor</p>
        </div>
    )
}