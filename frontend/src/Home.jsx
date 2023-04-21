
import React from 'react'
import HeroSection from './Components/HeroSection'
const Home = () => {
  const data = {
    name : "Documents Inventory App",
    image : "./Images/inventory1.webp",
  }
  return (
    // <div>Home</div>
    <HeroSection {...data} />

  )
}

export default Home







