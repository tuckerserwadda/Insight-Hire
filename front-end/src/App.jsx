import { useState } from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import Home from './Pages/Home/Home'
import ServerCheck from './components/SeverCheck'
import './App.css'

function App() {

  return (
    <>
     <nav>
      <Link to='/' >Home</Link> |  
       {/* <Link to='/server' >Check if Api is ok</Link> */}
     </nav>

     <Routes>
      <Route path='/' element={<Home/>}/>
      <Route path='/server' element={<ServerCheck/>}/>


     </Routes>
     
    </>
  )
}

export default App
