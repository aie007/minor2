import React from 'react'
import HeroSection from './Components/HeroSection'
const ProfileT = () => {
  const data = {
    name : "Teacher",
    image : "./Images/docs.png",
  }
  return (
    // <div>Home</div>
    <HeroSection {...data} />

  )
}

export default ProfileT