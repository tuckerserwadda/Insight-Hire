import { useState } from "react"

const JobDescription=() =>{
    const [description, setDescription] = useState('');
    const onClickSubmit = async(ev)=>{
        ev.preventDefault();
        if (!description.trim()) return;

        try{
            await fetch('http://127.0.0.1:8000/job/description',{
                method:'POST',
                header:{
                    'content-Type':'application/json',

                },
                body: JSON.stringify({
                    text:description,
                }),

            })
            
            setDescription('')
        }catch(error){
            console.error('system failed to submit job description', error)
        }
    }


    <>
    <h2>enter job  description </h2>

    <form onSubmit={onClickSubmit}>
        <textarea
        rows={6}
        value={des_text}
        onChange={(ev)=>setDescription(ev.target.value)}
        placeholder="paste jobdescription here .... "
        >

        </textarea>
    </form>
    </>
}
export default JobDescription