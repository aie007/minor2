import React from 'react'
import { Link, NavLink } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Alert from 'react-bootstrap/Alert' 

export default function Logout() {
    const [msg, setMsg] = useState('')
    const [show, setShow] = useState(false);
    const [success, setSuccess] = useState();

    const onSubmitClick = (e)=>{
        e.preventDefault()
        console.log("You pressed logout")
        fetch('/logout', {
          method: 'post',
          body: {}
        }).then(r => r.json())
            .then(result => {
              setSuccess(result.success);
              if(result.success) {
                  var message = 'Yeesss ' + result.user.username + '. OOya!';
                  setMsg(message);
                  setShow(true);
              }
              else {
                  var message = result.msg + '. Please try again!';
                  setMsg(message);
                  setShow(true);
              }
          })
          .catch((error) => {
            if (error.response) {
                console.log(error.response)
                console.log(error.response.status)
                console.log(error.response.headers)
                }
          })
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
            <h2 style={{color: "lightseagreen"}}>Do you wish to logout?</h2>
            <br />
            <br />
            <h3 ></h3>
            <form action="#">                
                <p>
                    <button id="sub_btn" type="submit" onClick={onSubmitClick}>Yes, log me out</button>
                </p>
                <p><Link to="/">No, go back to Home</Link>.</p>
            </form>
            <footer>
            </footer>
        </div>
      </div>
    )

}