import { useState } from "react"

const JobDescription=() =>{


    <>
    <h2>enter job  description </h2>

    <form onSubmit={onClickSubmit}>
        <textarea
        rows={6}
        value={des_text}
        onChange={(ev)=>setDescription(ev.target.value)}
        >

        </textarea>
    </form>
    </>
}
export default JobDescription