import {useEffect} from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import clsx from "clsx"
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

    console.log("percentage", user.completion_percentage)
    console.log("Employment", user.employment_status)
    console.log("Education", user.education)

    let message = null
    if (user.completion_percentage === 0){
        message = `👋 Let's get you started, ${user.name}`
    }
    else if (user.completion_percentage < 60){
        message = "🌱 You're making progress, keep going!"
    }
    else if(user.completion_percentage < 100){
        message = "🔥 Almost there — you're so close!"
    }
    else{
        message = " ⭐ Your profile is complete — you're ready!"
    }

    return (
        <div className='dashboard-container'>
            <div>
            <h2>Welcome back, {user.name} 👋</h2>
        </div>
        <div className='completion-card'>
            <div className="completion-layout">
                <div className="completion-content">
                    <h3> {message} </h3>

                    { user.completion_percentage < 100 ?
                            <p>A complete profile helps mentors understand your journey 
                                    and connect with you better.</p>
                            : <p>Mentors can now see your full story. 
                                    You're set up for success.</p>
                        }
                    <div className='step-indicators'>
                        <span 
                        className={clsx("badge", 
                            user.employment_status? "badge-dark" : "badge-light")}>
                        Employment</span>
                        <span 
                        className={clsx("badge", 
                            user.education? "badge-dark" : "badge-light")}>
                        Education</span>
                        <span className={clsx("badge",
                            user.projects ? "badge-dark" : "badge-light")}>
                        Projects</span>
                        <span className={clsx("badge",
                            user.gap_story ? "badge-dark" : "badge-light")}>
                        Gap Story</span>
                        <span className={clsx("badge",
                            user.gap_duration ? "badge-dark" : "badge-light")}>
                        Gap Duration</span>
                    </div>

                    <div className="progress">
                        <div
                            className="progress-bar"
                            style={{ width: `${user.completion_percentage}%` }}
                        />
                    </div>

                    {user.completion_percentage < 100 && (
                        <a href="/profile" className="continue-btn">
                            Continue Profile →
                        </a>
                    )}
                </div>
            
                <div className="percentage-circle">
                    <span className="percentage-value">
                        {user.completion_percentage}%
                    </span>
                    <span className="percentage-label">complete</span>
                </div>
        </div>
        </div>
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