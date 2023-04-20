import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Alert from 'react-bootstrap/Alert' 

import './Loginform.css'
export default function Login() {
    const [email, setEmail] = useState('')
    const [pwd, setPwd] = useState('')
    const [msg, setMsg] = useState('')
    const [show, setShow] = useState(false);
    const [success, setSuccess] = useState();

    const onSubmitClick = (e)=>{
        e.preventDefault()
        console.log("You pressed login")
        let opts = {
          'email': email,
          'pwd': pwd
        }
        console.log(opts)
        fetch('/login', {
          method: 'post',
          body: JSON.stringify(opts)
        }).then(r => r.json())
            .then(result => {
              setSuccess(result.success);
              if(result.success) {
                  var message = 'Welcome ' + result.user.username + '. OOya!';
                  setMsg(message);
                  setShow(true);
              }
              else {
                  var message = result.msg + '. Please try again!';
                  setMsg(message);
                  setShow(true);
              }
          })
      }

      const handleEmailChange = (e) => {
        setEmail(e.target.value)
      }

      const handlePwdChange = (e) => {
        setPwd(e.target.value)
      }

    return (
      <div>
        { success == true &&
                <center><Alert variant="success" onClose={() => setShow(false)} dismissible>
                    <Alert.Heading>Viola!</Alert.Heading>
                    <p>{msg}</p>
                </Alert></center>
            }
            {
                success == false &&
                <center><Alert variant="danger" onClose={() => setShow(false)} dismissible>
                    <Alert.Heading>Aw Snap!</Alert.Heading>
                    <p>{msg}</p>
                </Alert></center>
            }
        <div className="text-center m-5-auto">
            <h2 style={{color: "lightseagreen"}}>Login Here!</h2>
            <br />
            <br />
            <h3 ></h3>
            <form action="#">
                <p>
                    <label style={{color: "darkorchid"}}>Email</label><br/>
                    <input type="email" name="email" onChange={handleEmailChange} value={email}  required />
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Password</label><br/>
                    <input type="password" name="pwd" onChange={handlePwdChange} value={pwd}  required />
                </p>
                <br />
                <p>
                    <button id="sub_btn" type="submit" onClick={onSubmitClick}>Login</button>
                </p>
            </form>
            <footer>
                <p><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
      </div>
    )

}