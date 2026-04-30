import {useState} from 'react'
import { useNavigate } from 'react-router-dom'
import '../App.css'

export default function Login(){

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError('')

        try {
            const response = await fetch('http://127.0.0.1:8000/api/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            })

            const data = await response.json()
            console.log('Response data:', data)

            if (response.ok) {
                localStorage.setItem('access', data.access)
                localStorage.setItem('refresh', data.refresh)
                navigate('/dashboard')
            } else {
                setError('Invalid email or password')
            }
        } catch (err) {
            console.log('Error:', err)
            setError('Something went wrong. Please try again.')
        } finally {
            setLoading(false)
        }
}

    return(
        <div className="login-container">
            <div className="login-card">
                <div className="login-logo">⚡ Reboot</div>
                <h1 className="login-title">Welcome back</h1>
                <p className="login-subtitle">
                    Log in to continue your journey
                </p>
                {error && <div className="error-message">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input type="email" placeholder="you@example.com"
                        value={email} onChange = {e => setEmail(e.target.value)}
                        required/>
                    </div>
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" placeholder="••••••••"
                        value={password} onChange = {e => setPassword(e.target.value)}
                        required/>
                    </div>    
                    <button type="submit" className="btn-primary"
                    disabled={loading}> {loading ? 'Loggging in..': 'Log In'} </button>
                </form>
                <div className="login-footer">
                    Don't have an account? <a href="/register">Sign up</a>
                </div>
            </div>
        </div>
    )
}