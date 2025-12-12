import { useState } from "react";

const TYPES_ALLOWED = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    
]

const MAX_FiLE_SIZE = 10



const UploadResume = ()=>{
    const [error, setError] = useState('')
const [status, setStatus] = useState('')
const [uploadedFile, setUploadedFile] = useState(null)
const [isFileUploading, setIsFileUploading] = useState(false)
const [candidateSkills, setCandidateSkills] = useState([])
    
    // selecting file
    const onFileChange= (ev)=>{
        setError('')
        setStatus('')

        const fileSelected = ev.target.files[0];
        if(!fileSelected){
            setUploadedFile(null)
            return; 
        }
// check file type
        if(!TYPES_ALLOWED.includes(fileSelected.type)){
            setError('please check fileformat only pdf and word doccuments allowed')
            setUploadedFile(null)
            return
        }
 // check file size

        const fileSize = fileSelected.size / (1024 * 1024);
        if (fileSize > MAX_FiLE_SIZE){
            setError(`file too large, maximum size allowed ${MAX_FiLE_SIZE}`)
            setUploadedFile(null)
        }

        setUploadedFile(fileSelected)
    }

    // submit uploaded file 

    const onClickSubmit = async(ev)=>{
        ev.preventDefault();
        setError('')


 // check if file is not uploaded
        if(!uploadedFile){
            setError('invalid file selected please try again')
            return
        }

// upload file 

        try{
            setIsFileUploading(true);
            const fileData = new FormData();
            fileData.append('file', uploadedFile)
            const resp = await fetch('http://127.0.0.1:8000/resume/upload',{
                method: 'POST',
                body:fileData
            })

            if(!resp.ok){
                const dataError = await reportError.json().catch(()=>({}))
                throw new Error(dataError.detail || 'system failed to upload file')
            }

            const uploadedData = await resp.json();
            setStatus(`file uploaded successfully and recieved file ${uploadedData.filename}(${uploadedData.size}) mb`);
            console.log(uploadedData.skills)
            setCandidateSkills(uploadedData.skills || [])


        }catch(error){
        setError(`Error: ${error.message}`)
        }finally{
            setIsFileUploading(false);
        }



    }

    return(
        <div>
            <h2>Upload Resume: </h2>
            <p>accepted formats: PDF, DOC DOCX. and maximum size = 10mb</p>
            <div>
                <form onSubmit={onClickSubmit}>
                    <input type="file" onChange={onFileChange}/>

                    <button 
                    type="submit"
                    disabled = {isFileUploading || !uploadedFile}
                    > {isFileUploading? 'uploading File ...': 'Upload File'}</button>


                </form>

                {
                    status &&(
                        <p>{status}</p>
                    )}
                   { error &&<p>{error}</p>}
                   {candidateSkills.length > 0 && (
                    <div>
                        <h2> Candidate skills</h2>
                        <ul>
                           {candidateSkills.map((skill)=>(
                            <li key = {skill}>{candidateSkills}</li> 

                           ))} 
                        </ul>
                    </div>
                   )}
                
            </div>
        </div>
    )
}
export default UploadResume