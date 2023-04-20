import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'

import './Loginform.css'
export default function Register() {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [type, setType] = useState('teacher')
    const [pwd, setPwd] = useState('')
    const [cnfpwd, setCnfpwd] = useState('')

    const onSubmitClick = (e)=>{
        e.preventDefault()
        console.log("You pressed register")
        let opts = {
          'username': username,
          'email': email,
          'type': type,
          'pwd': pwd,
          'cnfpwd': cnfpwd
        }
        console.log(opts)
        fetch('/register', {
          method: 'post',
          body: JSON.stringify(opts)
        }).then(r => r.json())
            .then(success => {
                if(success.success)
                    console.log(success.msg)
                else
                    console.log(success.msg)
          })
      }
    
      const handleUsernameChange = (e) => {
        setUsername(e.target.value)
      }
    
      const handleEmailChange = (e) => {
        setEmail(e.target.value)
      }

      const handleTypeChange = (e) => {
        setType(e.target.value)
      }
      
      const handlePwdChange = (e) => {
        setPwd(e.target.value)
      }

      const handleCnfpwdChange = (e) => {
        setCnfpwd(e.target.value)
      }

    return (
        <div className="text-center m-5-auto">
            <h2 style={{color: "lightseagreen"}}>Join us!</h2>
            <br />
            <br />
            <h3 style={{color: "darkslateblue"}}>Create your personal account</h3>
            <form action="#">
                <p>
                    <label style={{color: "darkorchid"}}>Username</label><br/>
                    <input type="text" name="username" onChange={handleUsernameChange} value={username}  required />
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Email address</label><br/>
                    <input type="email" name="email" onChange={handleEmailChange} value={email}  required />
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Are you a Teacher or a Student?</label><br/>
                    <select name="type" id="type" onChange={handleTypeChange}  required>
                        <option value="teacher">Teacher</option>
                        <option value="student">Student</option>
                    </select>
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Password</label><br/>
                    <input type="password" name="pwd" onChange={handlePwdChange} value={pwd}  required />
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Confirm Password</label><br/>
                    <input type="password" name="cnfpwd" onChange={handleCnfpwdChange} value={cnfpwd} required />
                </p>
                <br />
                <h6>
                    <input type="checkbox" name="checkbox" id="checkbox" required /> <span>I agree all statements in <a href="https://google.com" target="_blank" rel="noopener noreferrer">terms of service</a></span>.
                </h6>
                <p>
                    <button id="sub_btn" type="submit" onClick={onSubmitClick}>Register</button>
                </p>
            </form>
            <footer>
                <p style={{textAlign: "center"}} ><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
    )

}