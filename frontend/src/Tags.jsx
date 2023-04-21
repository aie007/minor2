import React from 'react'
import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Alert from 'react-bootstrap/Alert' 

import './Loginform.css'
export default function Tags(props) {
    const [name, setName] = useState('')
    const [type, setType] = useState('domain')
    const [msg, setMsg] = useState('')
    const [show, setShow] = useState(false);
    const [success, setSuccess] = useState();

    const onSubmitClick = (e)=>{
        e.preventDefault()
        console.log("You pressed add")
        let opts = {
          'name': name,
          'type': type
        }
        console.log(opts)
        fetch('/tags', {
          method: 'post',
          body: JSON.stringify(opts)
        }).then(r => r.json())
            .then(result => {
              setSuccess(result.success);
              if(result.success) {
                  var message = 'YESSSS ' + result.msg + '. OOya!';
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

      const handleNameChange = (e) => {
        setName(e.target.value)
      }

      const handleTypeChange = (e) => {
        setType(e.target.value)
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
            <h2 style={{color: "lightseagreen"}}>Tags</h2>
            <br />
            <br />
            <h3 ></h3>
            <form action="#">
                <p>
                    <label style={{color: "darkorchid"}}>Tag Name</label><br/>
                    <input type="text" name="name" onChange={handleNameChange} value={name}  required />
                </p>
                <p>
                    <label style={{color: "darkorchid"}}>Tag Type</label><br/>
                    <select name="type" id="type" onChange={handleTypeChange}  required>
                            <option value="domain">Domain</option>
                            <option value="issued_by">Issued by</option>
                    </select>
                </p>
                <br />
                <p>
                    <button id="sub_btn" type="submit" onClick={onSubmitClick}>Add tag</button>
                </p>
            </form>
            <footer>
                <p><Link to="/">Back to Homepage</Link>.</p>
            </footer>
        </div>
      </div>
    )

}