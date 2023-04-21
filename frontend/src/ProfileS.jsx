import React from 'react'
import HeroSection from './Components/HeroSection'
const ProfileS = () => {
  const data = {
    name : "Student",
    image : "./Images/docs.png",
  }
  return (
    // <div>Home</div>
    <HeroSection {...data} />

  )
}

export default ProfileS