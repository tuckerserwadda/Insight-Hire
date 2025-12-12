import { useEffect, useState } from 'react';

const ServerCheck= ()=>{

    const [serverApiStatus, setServerApiStatus] = useState(null)
    const [message, setMesssage] = useState('')
    const [error, setError] = useState('')
    const [Loading, setLoading] = useState(true)

    useEffect(()=>{
        fetch('http://127.0.0.1:8000/server')
        .then((resp)=>{
            if (!resp.ok) throw new Error ('Network problem ');
            return resp.json();
        })
        .then((data)=>{
            setServerApiStatus(data.status);
            setMesssage(data.message)
            setLoading(false)
        })
        .catch((error)=>{
            setError(error.message)
            setLoading(false)

        })

    },[])

     if (Loading) return <h1> Server  checkoing ......</h1>
     if (error) return <p style = {{color: 'red'}}> Error : {error}</p>

    return(
        <>
        <div>
            <h1>status: <p>{serverApiStatus}</p></h1>
            <h1>message: <p>{message}</p></h1>
        </div>
        </>
    )
}

export default ServerCheck;