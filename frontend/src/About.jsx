import React from 'react'
import HeroSection from './Components/HeroSection'

const About = () => {

  const data = {
    name :"Inventory",
    image: "./Images/inventory.jpeg",
  }
  return (
    
    <HeroSection {...data} />
  )
}

export default About