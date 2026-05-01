import {useState} from 'react'
import { useNavigate } from 'react-router-dom'
import '../App.css'

export default function Register(){

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [role, setRole] = useState('')
    const [phone, setPhone] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const navigate = useNavigate()

    async function handleSubmit(e){
        e.preventDefault()
        setLoading(true)
        setError('')

        try{
            const response = await fetch('http://127.0.0.1:8000/api/auth/register/', {
                method : 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name, email, password, role })

            })

            const data = await response.json()

            if(response.ok){
                navigate('/login')
            }
            else {
               setError(data.message || 'Registration failed. Please try again.')
            }
        }
        catch (err){
            console.log('Error', err)
            setError('Something went wrong. Please try again.')
        }
        finally{
            setLoading(false)
        }
    }

    return(
    <div className="register-container">
        <div className="register-card">
            <div className="login-logo">⚡ Reboot</div>
                <h1 className='register-title'>Create your account</h1>
                <p className='register-subtitle'>Fill in your details</p>
                {error && <div className="error-message">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <div className='form-group'>
                        <label>Full Name</label>
                        <input type="text" value={name} placeholder='Your full name' 
                        onChange={e => setName(e.target.value)} required/>
                    </div>  
                    <div className='form-group'>
                        <label>Email</label>
                        <input type="email" value={email} placeholder='you@example.com' 
                        onChange={e => setEmail(e.target.value)} required/>
                    </div> 
                    <div className='form-group'>
                        <label>Phone Number</label>
                        <input type="text" value={phone} placeholder='+91 0000-000-000' 
                        onChange={e => setPhone(e.target.value)}/>
                    </div> 
                    <div className="form-group">
                        <label>Password</label>
                        <input type="password" placeholder="••••••••"
                        value={password} onChange = {e => setPassword(e.target.value)}
                        required/>
                    </div>
                    <div className='form-group'>
                        <label>Role</label>
                        <select value={role} 
                        onChange = {e => setRole(e.target.value)} required>
                            <option value="">Select your role</option>
                            <option value="career_gaper">Career Gaper</option>
                            <option value="mentor">Mentor</option>
                        </select>
                    </div>    
                    <button type="submit" className="btn-primary"
                    disabled={loading}> {loading ? "Creating..." : "Create Account"} </button>                 
                </form>
                <div className="register-footer">
                    Already have an account? <a href="/login">Sign in</a>
                </div>
        </div>
    </div>      
    )

}