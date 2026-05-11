import {useEffect, useState} from 'react'
import '../components/TrendsWidget.css'
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid
} from 'recharts'

function GrowthBadge({ growth }) {
    if (growth === null || growth === undefined) {
        return <span className="growth growth--neutral">—</span>
    }
    
    const arrow = growth > 0 ? '↑' : growth < 0 ? '↓' : '→'
    const modifier = growth > 0 ? 'up' : growth < 0 ? 'down' : 'neutral'
    
    return (
        <span className={`growth growth--${modifier}`}>
            {arrow} {Math.abs(growth).toFixed(1)}%
        </span>
    )
}

export default function TrendsWidget(){

    const [trends, setTrends] = useState(null)
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(true)
    const[currentIndex, setCurrentIndex] = useState(0)

    useEffect(()=>{

        async function fetchRequests(){
            try{
                const response = await fetch('http://127.0.0.1:8000/api/trends/latest/',{
                    headers:{
                        'Authorization': `Bearer ${localStorage.getItem('access')}`
                    }
                })
                if( response.ok){
                    const data = await response.json()
                    setTrends(data)
                }
                else{
                    setError(`Server returned ${response.status}`)
                }
            }catch (error) {
            setError(error.message)
            setLoading(false)
            }
            finally {
                setLoading(false)
            }
        }
        fetchRequests()
    },[])

    if (loading) return <div>Loading trends...</div>
    if (error)   return <div>Couldn't load trends: {error}</div>
    if (!trends || !trends.snapshot_date) return <div>Trends will appear soon.</div>

    const chartSlides = [
        { title: 'Top Skills',     data: trends.trends.skills },
        { title: 'Top Companies',  data: trends.trends.companies },
        { title: 'Top Roles',      data: trends.trends.roles },
    ]

    const nextSlide = () => {
        setCurrentIndex(
            (prev) => (prev + 1) % chartSlides.length
        )
    }

    const prevSlide = () => {
        setCurrentIndex(
            (prev) =>
                prev === 0
                    ? chartSlides.length - 1
                    : prev - 1
        )
    }

    const currentChart = chartSlides[currentIndex]
    
    return(
        <div className='trend-widget-container'>

            <h2>Job Trends</h2>
            <p>Snapshot: {trends.snapshot_date} • {trends.sample_size} listings</p>
            
            <h3>{currentChart.title}  ({currentIndex + 1} of {chartSlides.length})</h3>
            
                <BarChart width={700} height={300} data={currentChart.data.slice(0, 10)}>
                    <CartesianGrid />
                    <XAxis dataKey="name" 
                        interval={0}
                        angle={-30}
                        textAnchor="end"
                        height={70}
                        tickFormatter={(value) => value.length > 12 ? value.slice(0, 11) + '…' : value}/>
                    <YAxis 
                    tickFormatter={(value) => `${value}%`}/>
                    <Tooltip 
                        formatter={(value) => [`${value}%`, 'Listings']}
                        labelStyle={{ color: '#374151', fontWeight: 600 }}
                    />
                    <Bar dataKey="percentage" fill="#3b82f6" />
                </BarChart>

                <ul className="trends-list">
                    {currentChart.data.slice(0, 10).map(item => (
                        <li key={item.name} className="trends-list__item">
                            <span className="trends-list__name">{item.name}</span>
                            <span className="trends-list__stats">
                                <span className="trends-list__percent">{item.percentage}%</span>
                                <GrowthBadge growth={item.growth_7d} />
                            </span>
                        </li>
                    ))}
                </ul>

                <div className="nav-buttons">
                    <button onClick={prevSlide}>← Previous</button>
                    <button onClick={nextSlide}>Next →</button>
                </div>
        </div>
    )
}